/**
 * Rig Diagram Renderer
 * Dynamically generates an illustrated vector SVG diagram matching the exact
 * sequential order of components in the user's rig chain (Rod -> Reel -> Lines -> Knots -> Hardware -> Tippets -> Flies).
 */

window.RigDiagramRenderer = (function() {
    'use strict';

    // Color Palette
    const COLORS = {
        bgGradStart: '#090f1a',
        bgGradMid: '#0f172a',
        bgGradEnd: '#172554',
        rodCork: '#d4b08c',
        rodBlank: '#334155',
        rodGuide: '#cbd5e1',
        reelGrad: '#475569',
        flyLine: '#f59e0b',       // Amber Gold
        flyLineGlow: 'rgba(245, 158, 11, 0.45)',
        leader: '#ef4444',        // Vibrant Coral / Red
        leaderGlow: 'rgba(239, 68, 68, 0.45)',
        tippet: '#22c55e',        // Neon Lime Green
        tippetGlow: 'rgba(34, 197, 94, 0.45)',
        backing: '#06b6d4',       // Cyan
        knotBg: '#0f172a',
        knotBorder: '#e2e8f0',
        hardwareBg: '#1e293b',
        hardwareBorder: '#cbd5e1',
        indicator: '#ff1a53',
        splitShot: '#94a3b8',
        dropperLine: '#14b8a6',
        flyAccent: '#f59e0b'
    };

    /**
     * Categorizes a step into its structural rig type
     */
    function categorizeStep(item) {
        const cat = (item.category || '').toLowerCase();
        const name = (item.name || '').toLowerCase();

        // 1. Fly Rod & Reel
        if (cat.includes('rod') || name.includes('rod')) return 'rod';
        if (cat.includes('reel') || name.includes('reel')) return 'reel';

        // 2. Lines (Fly Line, Backing, Leader, Tippet) - MUST check lines before flexible attachments
        if (cat.includes('fly_line') || cat.includes('fly line') || cat === 'line' || cat.includes('flyline') || 
            name.includes('fly line') || name.includes('flyline') || cat.startsWith('line') || cat.endsWith('line')) {
            return 'fly_line';
        }
        if (cat.includes('backing') || name.includes('backing')) return 'backing';
        if (cat.includes('leader') || name.includes('leader')) return 'leader';
        if (cat.includes('tippet') && !name.includes('tippet ring') && !name.includes('ring') && !cat.includes('hardware')) return 'tippet';

        // 3. Knots
        if (cat.includes('knot') || name.includes('knot') || name.includes('loop')) return 'knot';

        // 4. In-line Hardware (Tippet rings, Swivels, Snaps)
        if (cat.includes('in-line') || cat.includes('inline') || name.includes('tippet ring') || name.includes('swivel') || name.includes('snap') || (cat.includes('hardware') && !cat.includes('flexible'))) return 'hardware';

        // 5. Flexible Hardware (Strike Indicators, Split Shot, Floats, Bobbers)
        if (cat.includes('flexible') || name.includes('indicator') || name.includes('split shot') || name.includes('splitshot') || name.includes('bobber') || (name.includes('float') && !name.includes('flyline') && !name.includes('fly line'))) return 'flexible_hardware';

        // 6. Flies
        if (cat.includes('fly') || cat.includes('hook') || cat.includes('bug') || name.includes('fly') || name.includes('midge') || name.includes('nymph') || name.includes('streamer') || name.includes('dry') || name.includes('wet') || name.includes('bugger') || name.includes('chironomid')) return 'fly';

        return 'other';
    }

    /**
     * Parses the sequential chain items
     */
    function parseSequentialChain(chainItems) {
        const result = {
            rod: null,
            reel: null,
            sequence: [] // Sequential items following rod & reel
        };

        (chainItems || []).forEach((item, index) => {
            const role = categorizeStep(item);
            const stepObj = Object.assign({}, item, {
                chainIndex: index + 1,
                role: role
            });

            if (role === 'rod' && !result.rod) {
                result.rod = stepObj;
            } else if (role === 'reel' && !result.reel) {
                result.reel = stepObj;
            } else {
                result.sequence.push(stepObj);
            }
        });

        return result;
    }

    /**
     * Smooth 2D Serpentine Path Waypoints across a 1100x640 canvas
     * Trajectory flows out from rod tip guide at (800, 54)
     */
    const PATH_WAYPOINTS = [
        { x: 450, y: 54 },    // 0: Rod tip exit (rod is from x=20 to x=450)
        { x: 650, y: 54 },    // 1: Fly line casting horizontally across top
        { x: 840, y: 58 },    // 2: Fly line extending towards top right
        { x: 960, y: 80 },    // 3: Fly line entering upper turn
        { x: 990, y: 145 },   // 4: Fly line curving around apex
        { x: 920, y: 215 },   // 5: Fly line sweeping down-left
        { x: 770, y: 265 },   // 6: Transition 1: #4 Loop knot (Fly line -> Leader)
        { x: 570, y: 320 },   // 7: Mid Leader (🔴 Strike Indicator with 📍 7ft from last fly)
        { x: 380, y: 380 },   // 8: Transition 2: #6 In-line Tippet Ring (Leader -> Tippet)
        { x: 210, y: 440 },   // 9: Tippet sweeping down-left
        { x: 95,  y: 505 },   // 10: Tippet lower-left turn apex
        { x: 220, y: 565 },   // 11: Tippet sweeping right across bottom
        { x: 520, y: 565 },   // 12: Tippet bottom tier
        { x: 800, y: 565 },   // 13: Tippet bottom tier
        { x: 980, y: 565 }    // 14: Terminal Point (Tag End / Fly)
    ];

    /**
     * Interpolates (x, y) coordinates along the serpentine path for t in [0, 1]
     */
    function getPointOnPath(t) {
        const clampedT = Math.max(0, Math.min(1, t));
        const numSegments = PATH_WAYPOINTS.length - 1;
        const scaled = clampedT * numSegments;
        const segIndex = Math.min(Math.floor(scaled), numSegments - 1);
        const segFraction = scaled - segIndex;

        const p0 = PATH_WAYPOINTS[Math.max(0, segIndex - 1)];
        const p1 = PATH_WAYPOINTS[segIndex];
        const p2 = PATH_WAYPOINTS[Math.min(numSegments, segIndex + 1)];
        const p3 = PATH_WAYPOINTS[Math.min(numSegments, segIndex + 2)];

        const x = catmullRom(p0.x, p1.x, p2.x, p3.x, segFraction);
        const y = catmullRom(p0.y, p1.y, p2.y, p3.y, segFraction);

        return { x: Math.round(x), y: Math.round(y) };
    }

    function catmullRom(p0, p1, p2, p3, t) {
        const v0 = (p2 - p0) * 0.5;
        const v1 = (p3 - p1) * 0.5;
        const t2 = t * t;
        const t3 = t * t2;
        return (2 * p1 - 2 * p2 + v0 + v1) * t3 +
               (-3 * p1 + 3 * p2 - 2 * v0 - v1) * t2 +
               v0 * t + p1;
    }

    /**
     * Samples dense points along the path between tStart and tEnd to draw smooth SVG path
     */
    function getSvgSubPath(tStart, tEnd, stepsCount) {
        const steps = stepsCount || 16;
        let d = '';
        for (let i = 0; i <= steps; i++) {
            const t = tStart + (tEnd - tStart) * (i / steps);
            const pt = getPointOnPath(t);
            if (i === 0) {
                d += `M ${pt.x},${pt.y}`;
            } else {
                d += ` L ${pt.x},${pt.y}`;
            }
        }
        return d;
    }

    /**
     * Main Render Entrypoint
     */
    function render(containerId, chainItems) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (!chainItems || chainItems.length === 0) {
            container.innerHTML = `
                <div class="text-center py-5 text-muted bg-dark rounded border border-secondary">
                    <i class="bi bi-diagram-3 fs-1 text-info opacity-50 d-block mb-2"></i>
                    <h5 class="fw-bold text-light">No Rig Components Configured</h5>
                    <p class="small text-white-50 mb-0">Add a Rod, Reel, Line, Leader, Knots, and Flies to generate your illustrated diagram.</p>
                </div>
            `;
            return;
        }

        const parsedRig = parseSequentialChain(chainItems);
        const svg = generateSvg(parsedRig);
        container.style.position = 'relative';
        container.innerHTML = svg;

        // Custom Floating Glassmorphism Tooltip
        let tooltipEl = container.querySelector('.rig-custom-tooltip');
        if (!tooltipEl) {
            tooltipEl = document.createElement('div');
            tooltipEl.className = 'rig-custom-tooltip';
            tooltipEl.style.cssText = 'position: absolute; display: none; pointer-events: none; z-index: 1050; background: rgba(15, 23, 42, 0.96); border: 1px solid #38bdf8; border-radius: 8px; padding: 8px 12px; color: #f8fafc; font-size: 12px; line-height: 1.4; box-shadow: 0 10px 25px rgba(0,0,0,0.6); backdrop-filter: blur(8px); max-width: 280px; transition: opacity 0.12s ease;';
            container.appendChild(tooltipEl);
        }

        const interactiveNodes = container.querySelectorAll('[data-tip-title]');
        interactiveNodes.forEach(node => {
            node.addEventListener('mouseenter', function(e) {
                const title = node.getAttribute('data-tip-title') || '';
                const desc = node.getAttribute('data-tip-desc') || '';
                if (!title) return;

                tooltipEl.innerHTML = `
                    <div style="font-weight: 700; color: #38bdf8; margin-bottom: 2px;">${title}</div>
                    ${desc ? `<div style="font-size: 11px; color: #cbd5e1; opacity: 0.9;">${desc}</div>` : ''}
                `;
                tooltipEl.style.display = 'block';
                tooltipEl.style.opacity = '1';
                positionTooltip(e);
            });

            node.addEventListener('mousemove', function(e) {
                positionTooltip(e);
            });

            node.addEventListener('mouseleave', function() {
                tooltipEl.style.display = 'none';
                tooltipEl.style.opacity = '0';
            });
        });

        function positionTooltip(e) {
            const containerRect = container.getBoundingClientRect();
            let x = e.clientX - containerRect.left + 15;
            let y = e.clientY - containerRect.top + 15;

            if (x + 260 > containerRect.width) {
                x = e.clientX - containerRect.left - 270;
            }
            if (y + 80 > containerRect.height) {
                y = e.clientY - containerRect.top - 70;
            }

            tooltipEl.style.left = Math.max(10, x) + 'px';
            tooltipEl.style.top = Math.max(10, y) + 'px';
        }
    }

    /**
     * Determines line color and stroke width for a given role
     */
    function getLinePropsForRole(role) {
        if (role === 'fly_line') return { color: COLORS.flyLine, width: 5.5, role: 'fly_line' };
        if (role === 'leader') return { color: COLORS.leader, width: 3.8, role: 'leader' };
        if (role === 'tippet') return { color: COLORS.tippet, width: 2.8, role: 'tippet' };
        if (role === 'backing') return { color: COLORS.backing, width: 4.5, role: 'backing' };
        return { color: COLORS.flyLine, width: 4.0, role: 'fly_line' };
    }

    /**
     * Builds the complete SVG from the parsed sequential rig
     */
    function generateSvg(rig) {
        const width = 1100;
        const height = 640;

        const rodObj = rig.rod;
        const reelObj = rig.reel;
        const rodName = rodObj ? rodObj.name : 'Fly Rod';
        const reelName = reelObj ? reelObj.name : 'Fly Reel';
        const seq = rig.sequence; // All steps after rod & reel

        let svgHtml = `
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" class="w-100 h-auto rig-illustration-svg" style="border-radius: 12px; font-family: system-ui, -apple-system, sans-serif; user-select: none;">
            <defs>
                <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="${COLORS.bgGradStart}" />
                    <stop offset="50%" stop-color="${COLORS.bgGradMid}" />
                    <stop offset="100%" stop-color="${COLORS.bgGradEnd}" />
                </linearGradient>

                <linearGradient id="corkGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#edd5be" />
                    <stop offset="50%" stop-color="#d4b08c" />
                    <stop offset="100%" stop-color="#b8936f" />
                </linearGradient>

                <linearGradient id="reelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#64748b" />
                    <stop offset="50%" stop-color="#334155" />
                    <stop offset="100%" stop-color="#0f172a" />
                </linearGradient>

                <filter id="glowLine" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="2.0" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>

                <radialGradient id="indicatorGrad" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#ff80a0" />
                    <stop offset="40%" stop-color="#ff1a53" />
                    <stop offset="100%" stop-color="#990026" />
                </radialGradient>

                <radialGradient id="shotGrad" cx="30%" cy="30%" r="70%">
                    <stop offset="0%" stop-color="#e2e8f0" />
                    <stop offset="45%" stop-color="#94a3b8" />
                    <stop offset="100%" stop-color="#334155" />
                </radialGradient>

                <radialGradient id="ringGrad" cx="35%" cy="35%" r="65%">
                    <stop offset="0%" stop-color="#f8fafc" />
                    <stop offset="50%" stop-color="#cbd5e1" />
                    <stop offset="100%" stop-color="#475569" />
                </radialGradient>
            </defs>

            <!-- 1. Background Frame -->
            <rect width="${width}" height="${height}" fill="url(#bgGrad)" rx="12" />

            <!-- Atmospheric subtle depth grid -->
            <g opacity="0.06" stroke="#38bdf8" stroke-width="1" fill="none">
                <path d="M0,150 Q275,100 550,150 T1100,150" />
                <path d="M0,320 Q275,270 550,320 T1100,320" />
                <path d="M0,480 Q275,430 550,480 T1100,480" />
            </g>

            <!-- 2. Fly Rod & Reel Assembly (Top Horizontal Bar) -->
            ${renderRodAndReelAssembly(rodObj, reelObj, rodName, reelName)}

            <!-- 3. Dynamic Sequential Assembly along Serpentine Trajectory -->
            ${renderPhysicalRigSequence(seq)}

            <!-- 4. Interactive Legend at bottom -->
            <g transform="translate(30, 605)">
                <rect x="0" y="0" width="1040" height="26" rx="8" fill="rgba(15, 23, 42, 0.85)" stroke="#334155" stroke-width="1" />
                <g transform="translate(20, 17)">
                    <circle cx="0" cy="-4" r="5" fill="${COLORS.flyLine}" />
                    <text x="10" y="0" fill="#94a3b8" font-size="10" font-weight="bold">Fly Line</text>

                    <circle cx="110" cy="-4" r="5" fill="${COLORS.leader}" />
                    <text x="120" y="0" fill="#94a3b8" font-size="10" font-weight="bold">Leader</text>

                    <circle cx="210" cy="-4" r="5" fill="${COLORS.tippet}" />
                    <text x="220" y="0" fill="#94a3b8" font-size="10" font-weight="bold">Tippet</text>

                    <circle cx="300" cy="-4" r="5" fill="${COLORS.indicator}" />
                    <text x="310" y="0" fill="#94a3b8" font-size="10" font-weight="bold">Indicator (Flex)</text>

                    <circle cx="430" cy="-4" r="5" fill="${COLORS.splitShot}" />
                    <text x="440" y="0" fill="#94a3b8" font-size="10" font-weight="bold">Split Shot (Flex)</text>

                    <circle cx="560" cy="-4" r="5" fill="#cbd5e1" stroke="#334155" stroke-width="1" />
                    <text x="570" y="0" fill="#94a3b8" font-size="10" font-weight="bold">In-line Hardware</text>

                    <text x="980" y="0" text-anchor="end" fill="#38bdf8" font-size="10" font-weight="semibold">💡 Hover over nodes for specs</text>
                </g>
            </g>
        </svg>
        `;

        return svgHtml;
    }

    /**
     * Formats clean, highly descriptive line labels for real-world practical use
     * (e.g. "Leader - Fluorocarbon 6 lbs (5ft)", "Tippet - 4 lbs Fluorocarbon (5ft)")
     */
    function formatLineBadgeLabel(lineItem) {
        const role = lineItem.role || '';
        let cat = (lineItem.category || '').trim();
        if (!cat) {
            cat = role === 'fly_line' ? 'Fly Line' : role === 'leader' ? 'Leader' : role === 'tippet' ? 'Tippet' : role === 'backing' ? 'Backing' : 'Line';
        }
        if (cat.toLowerCase() === 'fly line' || cat.toLowerCase() === 'fly_line' || cat.toLowerCase() === 'flyline') cat = 'Fly Line';
        else if (cat.toLowerCase() === 'leader') cat = 'Leader';
        else if (cat.toLowerCase() === 'tippet') cat = 'Tippet';
        else if (cat.toLowerCase() === 'backing') cat = 'Backing';

        let rawName = (lineItem.name || '').trim();
        const len = (lineItem.length || '').trim();

        // Extract concise name before any redundant " - ..." or brand repetition if present
        let spec = rawName;
        if (spec.includes(' - ')) {
            const parts = spec.split(' - ');
            spec = parts[0].trim();
        }

        if (role === 'fly_line') {
            if (spec.toLowerCase().startsWith('floating flyline') || spec.toLowerCase().startsWith('floating fly line') || spec.toLowerCase() === 'floating') {
                spec = 'Floating';
            } else if (spec.toLowerCase().startsWith('sinking flyline') || spec.toLowerCase().startsWith('sinking fly line') || spec.toLowerCase() === 'sinking') {
                spec = 'Sinking';
            }
        }

        let label = '';
        if (spec && !spec.toLowerCase().includes(cat.toLowerCase())) {
            label = `${cat} - ${spec}`;
        } else if (spec) {
            label = spec;
        } else {
            label = cat;
        }

        if (len && !label.includes(`(${len})`)) {
            label += ` (${len})`;
        }

        return label;
    }

    /**
     * Renders Anatomically Correct Fly Rod, Mounted Reel, Underside Snake Guides & Line Path
     */
    function renderRodAndReelAssembly(rodObj, reelObj, rodName, reelName) {
        return `
        <g id="rodReelGroup">
            <!-- Fighting Butt -->
            <rect x="20" y="47" width="12" height="6" rx="2" fill="#475569" stroke="#334155" stroke-width="0.8" />

            <!-- Machined Reel Seat Barrel -->
            <rect x="32" y="46" width="44" height="8" rx="2" fill="#1e293b" stroke="#64748b" stroke-width="1" />
            <rect x="42" y="45" width="14" height="10" rx="1" fill="#475569" stroke="#94a3b8" stroke-width="0.8" />
            <line x1="46" y1="45" x2="46" y2="55" stroke="#94a3b8" stroke-width="0.8" />
            <line x1="50" y1="45" x2="50" y2="55" stroke="#94a3b8" stroke-width="0.8" />

            <!-- Reel Mounted Underneath Reel Seat -->
            <g id="reelAssembly" class="cursor-pointer" 
               data-tip-title="⚙️ Reel: ${escapeXml(reelName)}"
               data-tip-desc="Category: Reel | Attached to Reel Seat">
                <!-- Reel Foot / Stem Bracket Clamped to Reel Seat -->
                <polygon points="38,54 62,54 58,62 42,62" fill="#64748b" stroke="#94a3b8" stroke-width="1" />
                <rect x="48" y="62" width="8" height="10" fill="#475569" stroke="#64748b" stroke-width="1" />

                <!-- Reel Frame & Large Arbor Spool -->
                <g transform="translate(52, 88)">
                    <circle cx="0" cy="0" r="22" fill="url(#reelGrad)" stroke="#94a3b8" stroke-width="2" />
                    <circle cx="0" cy="0" r="16" fill="none" stroke="#64748b" stroke-dasharray="3,3" stroke-width="1.8" />
                    <circle cx="0" cy="0" r="8" fill="${COLORS.flyLine}" opacity="0.9" />
                    <circle cx="0" cy="0" r="3.5" fill="#0f172a" stroke="#cbd5e1" stroke-width="1" />
                    <circle cx="11" cy="-7" r="3.5" fill="#e2e8f0" stroke="#334155" stroke-width="1" />
                </g>
            </g>

            <!-- Contoured Cork Handle Grip (in front of reel seat) -->
            <g id="corkGripGroup">
                <rect x="76" y="43" width="92" height="14" rx="5" fill="url(#corkGrad)" stroke="#a17852" stroke-width="1" />
                <line x1="90" y1="43" x2="90" y2="57" stroke="#b8936f" stroke-width="1" opacity="0.6" />
                <line x1="110" y1="43" x2="110" y2="57" stroke="#b8936f" stroke-width="1" opacity="0.6" />
                <line x1="130" y1="43" x2="130" y2="57" stroke="#b8936f" stroke-width="1" opacity="0.6" />
                <line x1="150" y1="43" x2="150" y2="57" stroke="#b8936f" stroke-width="1" opacity="0.6" />
                <rect x="168" y="46" width="4" height="8" fill="#cbd5e1" stroke="#475569" stroke-width="0.8" />
            </g>

            <!-- Graphite Tapered Rod Blank (extends from x=172 to tip at x=450) -->
            <g id="rodBlankGroup" class="cursor-pointer" 
               data-tip-title="🎣 Fly Rod: ${escapeXml(rodName)}"
               data-tip-desc="Category: Fly Rod | High-Modulus Graphite Blank">
                <polygon points="172,49.5 450,50.2 450,51.8 172,52.5" fill="#334155" stroke="#475569" stroke-width="0.5" />
                <line x1="172" y1="50.2" x2="450" y2="50.8" stroke="#94a3b8" stroke-width="0.8" opacity="0.7" />
            </g>

            <!-- Snake Guides Mounted on the UNDERSIDE (Bottom) of the Blank -->
            ${renderUndersideGuides([210, 270, 330, 390, 435])}

            <!-- Tip-Top Guide at (450, 51) with Ring Loop at (450, 54) -->
            <rect x="446" y="50" width="5" height="2.5" fill="#cbd5e1" />
            <circle cx="450" cy="54" r="3" fill="none" stroke="#cbd5e1" stroke-width="1.5" />

            <!-- Fly Line emerging from Reel Spool along Underside Guides to Tip -->
            <path d="M70,84 C110,78 150,64 210,62 L270,59 L330,58 L390,57 L435,56 L450,54" 
                  fill="none" stroke="${COLORS.flyLine}" stroke-width="3" stroke-linecap="round" opacity="0.95" />

            <!-- Top Rod & Reel Header Badges -->
            <g transform="translate(60, 16)">
                <!-- Rod Badge -->
                <g class="cursor-pointer" 
                   data-tip-title="🎣 Fly Rod: ${escapeXml(rodName)}" 
                   data-tip-desc="Fly Rod">
                    <rect x="0" y="0" width="220" height="20" rx="10" fill="rgba(15, 23, 42, 0.92)" stroke="#38bdf8" stroke-width="1.2" />
                    <text x="12" y="14" fill="#38bdf8" font-size="10.5" font-weight="bold">🎣 Fly Rod: ${escapeXml(truncate(rodName, 22))}</text>
                </g>

                <!-- Reel Badge -->
                <g transform="translate(230, 0)" class="cursor-pointer" 
                   data-tip-title="⚙️ Reel: ${escapeXml(reelName)}" 
                   data-tip-desc="Reel">
                    <rect x="0" y="0" width="180" height="20" rx="10" fill="rgba(15, 23, 42, 0.92)" stroke="#94a3b8" stroke-width="1.2" />
                    <text x="12" y="14" fill="#f8fafc" font-size="10.5" font-weight="bold">⚙️ Reel: ${escapeXml(truncate(reelName, 18))}</text>
                </g>
            </g>
        </g>
        `;
    }

    /**
     * Renders Snake Guides hanging underneath the rod blank
     */
    function renderUndersideGuides(positions) {
        return positions.map((x, idx) => {
            if (idx === 0) {
                return `
                <g transform="translate(${x}, 52)">
                    <line x1="-3" y1="0" x2="0" y2="10" stroke="#cbd5e1" stroke-width="1.5" />
                    <line x1="3" y1="0" x2="0" y2="10" stroke="#cbd5e1" stroke-width="1.5" />
                    <circle cx="0" cy="10" r="3.5" fill="none" stroke="#94a3b8" stroke-width="1.8" />
                </g>
                `;
            }
            return `
            <g transform="translate(${x}, 51)">
                <line x1="-3" y1="0" x2="-1" y2="7" stroke="#cbd5e1" stroke-width="1.2" />
                <line x1="3" y1="0" x2="1" y2="7" stroke="#cbd5e1" stroke-width="1.2" />
                <path d="M-1,7 Q0,9 1,7" fill="none" stroke="#cbd5e1" stroke-width="1.2" />
            </g>
            `;
        }).join('');
    }

    /**
     * Physical Rig Segmentation & Rendering Engine
     * Partitions sequence into major physical Line Spans (Fly Line, Leader, Tippet)
     * and Connection Junctions (Knots, In-line Hardware) connecting them.
     */
    function renderPhysicalRigSequence(seq) {
        if (!seq || seq.length === 0) return '';

        let html = '';

        // 1. Group sequence into ordered Line Spans and the Junctions between them
        const spans = [];
        let currentJunction = [];

        seq.forEach(item => {
            const isLine = (item.role === 'fly_line' || item.role === 'leader' || item.role === 'tippet' || item.role === 'backing');
            if (isLine) {
                spans.push({
                    lineItem: item,
                    preJunction: currentJunction
                });
                currentJunction = [];
            } else {
                currentJunction.push(item);
            }
        });

        const postJunction = currentJunction;

        if (spans.length === 0) {
            return renderFallbackSequence(seq);
        }

        const M = spans.length;

        // 2. Allocate path parameters: Give Fly Line a prominent share across top & mid-turn
        const spanRanges = [];
        let curT = 0.0;
        for (let k = 0; k < M; k++) {
            let spanFrac;
            if (M === 3) {
                spanFrac = (k === 0) ? 0.428 : (k === 1 ? 0.143 : 0.429);
            } else if (M === 2) {
                spanFrac = (k === 0) ? 0.50 : 0.50;
            } else {
                spanFrac = 1.0 / M;
            }
            const tStart = curT;
            const tEnd = Math.min(1.0, curT + spanFrac);
            spanRanges.push({ tStart, tEnd, tMid: (tStart + tEnd) * 0.5 });
            curT = tEnd;
        }

        // 3. Render each Line Span and its preceding / succeeding junctions
        for (let k = 0; k < M; k++) {
            const span = spans[k];
            const range = spanRanges[k];
            const lineItem = span.lineItem;
            const props = getLinePropsForRole(lineItem.role);
            const hasAttachments = lineItem.attachments && Array.isArray(lineItem.attachments) && lineItem.attachments.length > 0;
            const lineLabel = formatLineBadgeLabel(lineItem);

            // A. Preceding Junction (knots / in-line hardware before this line span)
            if (span.preJunction && span.preJunction.length > 0) {
                const juncT = range.tStart;
                const prevRole = k > 0 ? spans[k - 1].lineItem.role : 'fly_line';
                html += renderJunctionGroup(span.preJunction, juncT, k, prevRole, lineItem.role);
            }

            // B. Draw Line Segment for this span
            const pathD = getSvgSubPath(range.tStart, range.tEnd, 16);
            
            // Intelligent badge placement along the line segment
            let badgeT;
            if (lineItem.role === 'fly_line') {
                badgeT = range.tStart + (range.tEnd - range.tStart) * 0.38; // Centered along top casting sweep
            } else if (lineItem.role === 'leader') {
                badgeT = hasAttachments 
                    ? (range.tStart + (range.tEnd - range.tStart) * 0.30) // Upper diagonal to leave clear room for indicator & knot loupe
                    : range.tMid;
            } else if (lineItem.role === 'tippet') {
                badgeT = range.tStart + (range.tEnd - range.tStart) * 0.65; // Bottom horizontal sweep
            } else {
                badgeT = range.tMid;
            }
            const ptBadge = getPointOnPath(badgeT);
            const badgeOffsetY = (lineItem.role === 'tippet') ? 18 : -20;

            // Calculate badge dimensions based on label length
            const badgeW = Math.max(130, Math.min(300, Math.round(lineLabel.length * 6.2 + 32)));
            const halfW = Math.round(badgeW / 2);

            html += `
            <g id="lineSpan_${lineItem.chainIndex}">
                <path d="${pathD}" fill="none" stroke="${props.color}" stroke-width="${props.width}" stroke-linecap="round" filter="url(#glowLine)" />
                
                <!-- Floating Line Badge -->
                <g transform="translate(${ptBadge.x}, ${ptBadge.y + badgeOffsetY})" class="cursor-pointer" 
                   data-tip-title="${getRoleEmoji(lineItem.role)} ${escapeXml(lineItem.category || lineItem.role)}: ${escapeXml(lineItem.name)}"
                   data-tip-desc="${lineItem.length ? `Length: ${escapeXml(lineItem.length)}` : 'Line Section'}">
                    <rect x="${-halfW}" y="-12" width="${badgeW}" height="24" rx="12" fill="rgba(15, 23, 42, 0.94)" stroke="${props.color}" stroke-width="1.8" />
                    <circle cx="${-halfW + 14}" cy="0" r="4.5" fill="${props.color}" />
                    <text x="8" y="4" text-anchor="middle" fill="#f8fafc" font-size="10" font-weight="bold">${escapeXml(lineLabel)}</text>
                </g>
            `;

            // C. Flexible Hardware Attachments (Strike Indicator / Split Shot)
            if (hasAttachments) {
                lineItem.attachments.forEach((att, attIdx) => {
                    const isInd = (att.type === 'indicator') || (att.name || '').toLowerCase().includes('indicator') || (att.name || '').toLowerCase().includes('float');
                    const attT = range.tStart + (range.tEnd - range.tStart) * 0.68;
                    const attPt = getPointOnPath(attT);
                    const distLabel = (att.distance || '').trim();

                    if (isInd) {
                        html += `
                        <g transform="translate(${attPt.x}, ${attPt.y - 10})" class="cursor-pointer" 
                           data-tip-title="🔴 Strike Indicator: ${escapeXml(att.name || 'Strike Indicator')}"
                           data-tip-desc="${escapeXml(distLabel || 'Strike indicator on line')}">
                            <!-- Glowing Indicator Bead directly on line -->
                            <circle cx="0" cy="0" r="14" fill="url(#indicatorGrad)" stroke="#ffffff" stroke-width="2" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.5))" />
                            <circle cx="-4" cy="-4" r="3.5" fill="#ffffff" opacity="0.6" />
                            <line x1="-10" y1="-10" x2="10" y2="10" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round" />
                            
                            <!-- Wide Unclipped Callout Badge: Indicator Name & Distance -->
                            <g transform="translate(0, 20)">
                                <rect x="-80" y="0" width="160" height="${distLabel ? '36' : '20'}" rx="10" fill="rgba(15, 23, 42, 0.96)" stroke="#ff1a53" stroke-width="1.5" filter="drop-shadow(0 3px 6px rgba(0,0,0,0.6))" />
                                <text x="0" y="14" text-anchor="middle" fill="#ff80a0" font-size="9.5" font-weight="bold">🔴 ${escapeXml(truncate(att.name || 'Strike Indicator', 22))}</text>
                                ${distLabel ? `
                                    <text x="0" y="28" text-anchor="middle" fill="#38bdf8" font-size="9" font-weight="bold">📍 ${escapeXml(truncate(distLabel, 24))}</text>
                                ` : ''}
                            </g>
                        </g>
                        `;
                    } else {
                        html += `
                        <g transform="translate(${attPt.x}, ${attPt.y - 12})" class="cursor-pointer" 
                           data-tip-title="⚖️ Split Shot: ${escapeXml(att.name || 'Split Shot')}"
                           data-tip-desc="${escapeXml(distLabel || 'Split shot on line')}">
                            <!-- Split Shot Leads on line -->
                            <circle cx="-3" cy="0" r="6" fill="url(#shotGrad)" stroke="#1e293b" stroke-width="1" />
                            <circle cx="5" cy="2" r="6" fill="url(#shotGrad)" stroke="#1e293b" stroke-width="1" />
                            
                            <!-- Split Shot Callout Badge -->
                            <g transform="translate(0, 16)">
                                <rect x="-65" y="0" width="130" height="${distLabel ? '32' : '18'}" rx="8" fill="rgba(15, 23, 42, 0.96)" stroke="#94a3b8" stroke-width="1.2" />
                                <text x="0" y="12" text-anchor="middle" fill="#e2e8f0" font-size="9" font-weight="bold">⚖️ ${escapeXml(truncate(att.name || 'Split Shot', 16))}</text>
                                ${distLabel ? `
                                    <text x="0" y="25" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">📍 ${escapeXml(truncate(distLabel, 20))}</text>
                                ` : ''}
                            </g>
                        </g>
                        `;
                    }
                });
            }

            html += `</g>`;
        }

        // 4. Render Post Junction (Terminal knots, flies, or Fly End)
        const lastRange = spanRanges[M - 1];
        if (postJunction && postJunction.length > 0) {
            html += renderJunctionGroup(postJunction, lastRange.tEnd, M, spans[M - 1].lineItem.role, 'terminal');
        } else {
            const endPt = getPointOnPath(lastRange.tEnd);
            html += `
            <g transform="translate(${endPt.x}, ${endPt.y})">
                <circle cx="0" cy="0" r="4.5" fill="#22c55e" stroke="#ffffff" stroke-width="1.8" filter="drop-shadow(0 0 6px rgba(34,197,94,0.8))" />
                <rect x="-45" y="8" width="90" height="18" rx="9" fill="#0f172a" stroke="#22c55e" stroke-width="1.2" />
                <text x="0" y="21" text-anchor="middle" fill="#86efac" font-size="9" font-weight="bold">✦ Fly End</text>
            </g>
            `;
        }

        return html;
    }

    /**
     * Renders a group of junction items (knots, in-line hardware, flies) at a connection point
     */
    function renderJunctionGroup(items, baseT, groupIndex, prevRole, nextRole) {
        if (!items || items.length === 0) return '';

        let html = '';
        const count = items.length;

        const prevColor = getLinePropsForRole(prevRole).color;
        const nextColor = getLinePropsForRole(nextRole).color;

        items.forEach((item, idx) => {
            const offsetFraction = (count === 1) ? 0 : (idx - (count - 1) * 0.5) * 0.035;
            const itemT = Math.max(0.02, Math.min(0.98, baseT + offsetFraction));
            const pt = getPointOnPath(itemT);

            const role = item.role;
            const name = item.name || item.category || 'Component';
            const cat = item.category || 'Gear';

            if (role === 'knot') {
                const isLoopKnot = (name.toLowerCase().includes('loop') || name.toLowerCase().includes('perfection'));
                const loupeX = 60;
                const loupeY = -45;

                html += `
                <g transform="translate(${pt.x}, ${pt.y})">
                    <!-- Knot Graphic directly on the line -->
                    ${isLoopKnot ? `
                        <!-- Interlocking Loop-to-Loop Knot Link -->
                        <g opacity="0.95">
                            <ellipse cx="-4" cy="0" rx="6" ry="3.5" fill="none" stroke="${prevColor}" stroke-width="2.5" />
                            <ellipse cx="4" cy="0" rx="6" ry="3.5" fill="none" stroke="${nextColor}" stroke-width="2.5" />
                        </g>
                    ` : `
                        <circle cx="0" cy="0" r="5.5" fill="#f59e0b" stroke="#ffffff" stroke-width="1.8" />
                    `}

                    <!-- Tether Line to Callout Loupe -->
                    <line x1="0" y1="0" x2="${loupeX}" y2="${loupeY}" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3" />

                    <!-- Knot Callout Loupe -->
                    <g transform="translate(${loupeX}, ${loupeY})" class="cursor-pointer" 
                       data-tip-title="🪢 Knot: ${escapeXml(name)}"
                       data-tip-desc="Line Transition Knot">
                        <circle cx="0" cy="0" r="30" fill="${COLORS.knotBg}" stroke="#f59e0b" stroke-width="2" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.5))" />
                        <circle cx="0" cy="0" r="26" fill="#1e293b" />
                        
                        <g transform="scale(0.65) translate(-22, -22)">
                            ${getKnotIconSvg(name)}
                        </g>

                        <rect x="-60" y="34" width="120" height="18" rx="9" fill="#0f172a" stroke="#f59e0b" stroke-width="1" />
                        <text x="0" y="47" text-anchor="middle" fill="#fef08a" font-size="9.5" font-weight="bold">${escapeXml(truncate(name, 18))}</text>
                    </g>
                `;

                if (item.dropper_branch && Array.isArray(item.dropper_branch) && item.dropper_branch.length > 0) {
                    html += renderDropperBranch(item.dropper_branch);
                }

                html += `</g>`;
            }

            else if (role === 'hardware') {
                const isRing = name.toLowerCase().includes('ring');
                const loupeX = -45;
                const loupeY = -45;

                html += `
                <g transform="translate(${pt.x}, ${pt.y})">
                    <!-- Thumbnail/Knot-Sized Hardware Connection Directly on the Line -->
                    ${isRing ? `
                        <!-- Metallic Tippet Ring (Thumbnail scale ~5px radius) -->
                        <g opacity="0.98">
                            <circle cx="0" cy="0" r="5" fill="url(#ringGrad)" stroke="#ffffff" stroke-width="1.3" />
                            <circle cx="0" cy="0" r="2.2" fill="#0f172a" stroke="#475569" stroke-width="0.8" />
                            <circle cx="-1.5" cy="-1.5" r="0.9" fill="#ffffff" opacity="0.8" />
                        </g>
                    ` : `
                        <!-- Micro Swivel (Thumbnail scale) -->
                        <g opacity="0.98">
                            <rect x="-3" y="-7" width="6" height="14" rx="2" fill="url(#ringGrad)" stroke="#ffffff" stroke-width="1.0" />
                            <circle cx="0" cy="-4.5" r="1.5" fill="#0f172a" />
                            <circle cx="0" cy="4.5" r="1.5" fill="#0f172a" />
                        </g>
                    `}

                    <!-- Tether Line to Callout Loupe -->
                    <line x1="0" y1="0" x2="${loupeX}" y2="${loupeY}" stroke="#64748b" stroke-width="1.5" stroke-dasharray="3,3" />

                    <!-- In-line Hardware Callout Loupe -->
                    <g transform="translate(${loupeX}, ${loupeY})" class="cursor-pointer" 
                       data-tip-title="💍 In-line Hardware: ${escapeXml(name)}"
                       data-tip-desc="Micro Structural Hardware (2-3mm) | Joins lines seamlessly">
                        <circle cx="0" cy="0" r="30" fill="${COLORS.hardwareBg}" stroke="#cbd5e1" stroke-width="2" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.5))" />
                        <circle cx="0" cy="0" r="26" fill="#0f172a" />
                        
                        <g transform="scale(0.85)">
                            ${isRing ? `
                                <circle cx="0" cy="0" r="14" fill="url(#ringGrad)" stroke="#ffffff" stroke-width="2.2" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.4))" />
                                <circle cx="0" cy="0" r="7" fill="#0f172a" stroke="#475569" stroke-width="1.2" />
                                <circle cx="-4" cy="-4" r="2.5" fill="#ffffff" opacity="0.7" />
                            ` : `
                                <rect x="-6" y="-13" width="12" height="26" rx="3" fill="url(#ringGrad)" stroke="#ffffff" stroke-width="1.8" />
                                <circle cx="0" cy="-8.5" r="3" fill="#0f172a" />
                                <circle cx="0" cy="8.5" r="3" fill="#0f172a" />
                            `}
                        </g>

                        <!-- In-line Hardware Label Badge -->
                        <rect x="-65" y="34" width="130" height="18" rx="9" fill="#0f172a" stroke="#cbd5e1" stroke-width="1" />
                        <text x="0" y="47" text-anchor="middle" fill="#f8fafc" font-size="9.5" font-weight="bold">${escapeXml(truncate(name, 18))}</text>
                    </g>
                `;

                if (item.dropper_branch && Array.isArray(item.dropper_branch) && item.dropper_branch.length > 0) {
                    html += renderDropperBranch(item.dropper_branch);
                }

                html += `</g>`;
            }

            else if (role === 'fly') {
                html += `
                <g transform="translate(${pt.x}, ${pt.y})" class="cursor-pointer" 
                   data-tip-title="🪰 Fly: ${escapeXml(name)}"
                   data-tip-desc="Terminal Fly Lure">
                    <g transform="translate(-10, -5) scale(0.9)">
                        ${getFlyArtworkSvg(COLORS.flyAccent)}
                    </g>
                    <rect x="-60" y="20" width="120" height="20" rx="6" fill="#1e293b" stroke="${COLORS.flyAccent}" stroke-width="1.5" />
                    <text x="0" y="34" text-anchor="middle" fill="#fef08a" font-size="10" font-weight="bold">🪰 ${escapeXml(truncate(name, 15))}</text>
                </g>
                `;
            }
        });

        return html;
    }

    /**
     * Fallback renderer if no line spans are present
     */
    function renderFallbackSequence(seq) {
        let html = '';
        const N = seq.length;
        seq.forEach((item, i) => {
            const t = (i / Math.max(1, N - 1)) * 0.94;
            const pt = getPointOnPath(t);
            html += `
            <g transform="translate(${pt.x}, ${pt.y})" class="cursor-pointer" 
               data-tip-title="${escapeXml(item.name || item.category)}">
                <circle cx="0" cy="0" r="6" fill="#38bdf8" stroke="#ffffff" stroke-width="1.5" />
                <rect x="-40" y="10" width="80" height="16" rx="8" fill="#0f172a" stroke="#38bdf8" stroke-width="1" />
                <text x="0" y="22" text-anchor="middle" fill="#38bdf8" font-size="8.5" font-weight="bold">${escapeXml(truncate(item.name || item.category, 14))}</text>
            </g>
            `;
        });
        return html;
    }

    /**
     * Renders a 'Y' Dropper Branch dropping down from a knot or in-line hardware
     */
    function renderDropperBranch(branchItems) {
        const flyItem = branchItems.find(it => (it.category || '').toLowerCase().includes('fly')) || branchItems[branchItems.length - 1];
        const lengthItem = branchItems.find(it => it.length);
        const branchLen = lengthItem ? lengthItem.length : '6in';
        const dropperFlyName = flyItem ? flyItem.name : 'Dropper Fly';

        return `
        <g>
            <path d="M0,0 C15,25 15,55 5,75" fill="none" stroke="${COLORS.dropperLine}" stroke-width="2.5" stroke-dasharray="4,2" />
            <g transform="translate(18, 38)">
                <rect x="0" y="-8" width="65" height="16" rx="8" fill="#0f172a" stroke="${COLORS.dropperLine}" stroke-width="1" />
                <text x="32" y="4" text-anchor="middle" fill="#5eead4" font-size="8.5" font-weight="bold">'Y' ${escapeXml(branchLen)}</text>
            </g>
            <g transform="translate(5, 75)" class="cursor-pointer" 
               data-tip-title="🪰 'Y' Dropper: ${escapeXml(dropperFlyName)}"
               data-tip-desc="Branch Length: ${escapeXml(branchLen)}">
                <g transform="translate(-10, -5) scale(0.75)">
                    ${getFlyArtworkSvg('#14b8a6')}
                </g>
                <rect x="-50" y="16" width="100" height="18" rx="6" fill="#1e293b" stroke="#14b8a6" stroke-width="1.5" />
                <text x="0" y="29" text-anchor="middle" fill="#5eead4" font-size="9" font-weight="bold">🪰 ${escapeXml(truncate(dropperFlyName, 11))}</text>
            </g>
        </g>
        `;
    }

    /**
     * Vector icon for knots
     */
    function getKnotIconSvg(knotName) {
        const k = (knotName || '').toLowerCase();
        if (k.includes('perfection') || k.includes('loop')) {
            return `
                <g stroke="#f59e0b" stroke-width="3" fill="none">
                    <circle cx="20" cy="30" r="10" />
                    <circle cx="36" cy="30" r="10" stroke="#ef4444" />
                    <line x1="6" y1="30" x2="50" y2="30" stroke="#ffffff" stroke-width="1.5" />
                </g>
            `;
        } else if (k.includes('blood') || k.includes('barrel')) {
            return `
                <g stroke="#f59e0b" stroke-width="2.5" fill="none">
                    <path d="M10,25 Q25,15 40,25 T60,25" stroke="#f59e0b" />
                    <path d="M10,35 Q25,45 40,35 T60,35" stroke="#ef4444" />
                    <line x1="28" y1="14" x2="28" y2="46" stroke="#f59e0b" stroke-width="2" />
                    <line x1="42" y1="14" x2="42" y2="46" stroke="#ef4444" stroke-width="2" />
                </g>
            `;
        } else if (k.includes('surgeon')) {
            return `
                <g stroke="#22c55e" stroke-width="3" fill="none">
                    <ellipse cx="28" cy="30" rx="14" ry="9" stroke="#ef4444" />
                    <ellipse cx="30" cy="30" rx="14" ry="9" stroke="#22c55e" stroke-dasharray="5,2" />
                    <line x1="6" y1="30" x2="50" y2="30" stroke="#ffffff" stroke-width="1.5" />
                </g>
            `;
        } else {
            return `
                <g stroke="#38bdf8" stroke-width="2.5" fill="none">
                    <path d="M15,30 C20,18 36,18 40,30 C36,42 20,42 15,30 Z" stroke="#38bdf8" />
                    <circle cx="15" cy="30" r="3.5" fill="#cbd5e1" />
                    <line x1="15" y1="30" x2="50" y2="30" stroke="#ffffff" stroke-width="2" />
                </g>
            `;
        }
    }

    /**
     * Vector Artwork for a Fly Lure (Hook bend, hackle, body, wing)
     */
    function getFlyArtworkSvg(accentColor) {
        return `
            <g>
                <path d="M5,10 L25,10 C32,10 36,15 36,22 C36,28 30,32 24,32 L20,32" 
                      fill="none" stroke="#cbd5e1" stroke-width="2.5" stroke-linecap="round" />
                <polygon points="20,32 23,28 22,34" fill="#cbd5e1" />
                <circle cx="5" cy="10" r="3" fill="none" stroke="#cbd5e1" stroke-width="2" />
                <ellipse cx="18" cy="10" rx="8" ry="4" fill="#78350f" stroke="${accentColor}" stroke-width="1" />
                <path d="M12,10 L8,2 M14,10 L12,1 M16,10 L16,0 M18,10 L20,1 M20,10 L24,2" 
                      stroke="${accentColor}" stroke-width="1.8" stroke-linecap="round" />
                <path d="M14,10 L32,4" stroke="#f1f5f9" stroke-width="2" stroke-linecap="round" opacity="0.9" />
                <path d="M25,10 L35,16" stroke="${accentColor}" stroke-width="1.5" stroke-linecap="round" />
            </g>
        `;
    }

    function getRoleEmoji(role) {
        if (role === 'fly_line') return '🟡';
        if (role === 'leader') return '🔴';
        if (role === 'tippet') return '🟢';
        if (role === 'backing') return '🔵';
        return '〰️';
    }

    function truncate(str, max) {
        if (!str) return '';
        return str.length > max ? str.substring(0, max - 1) + '…' : str;
    }

    function escapeXml(unsafe) {
        if (!unsafe) return '';
        return String(unsafe).replace(/[<>&'"]/g, function (c) {
            switch (c) {
                case '<': return '&lt;';
                case '>': return '&gt;';
                case '&': return '&amp;';
                case '\'': return '&apos;';
                case '"': return '&quot;';
            }
        });
    }

    return {
        render: render,
        generateSvg: generateSvg,
        parseSequentialChain: parseSequentialChain
    };
})();
