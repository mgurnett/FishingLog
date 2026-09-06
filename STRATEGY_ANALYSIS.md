# Fishing Strategy, Setup Sharing & Catch Log Integration Plan

---

## 1. Overall Vision & Data Flow

Connecting **Line Setup (Rig)** ➜ **Fishing Strategy (Technique & Retrieval)** ➜ **Catch Log** creates a complete feedback loop for analyzing fishing success and powering AI trip planning.

```
+---------------------------+       +-----------------------------------+
|     Line Setup (Rig)      | ----> |      Fishing Strategy (How)       |
| (Line, Leader, Tippets,   |       | (Technique, Retrieval, Cadence,   |
|  Knots, Indicator, Hooks) |       |  Depth, Wind, Target Water Temp)  |
+---------------------------+       +-----------------------------------+
              \                                      /
               \                                    /
                v                                  v
        +--------------------------------------------------+
        |                 Catch Log Entry                  |
        | (Date, Lake, Fish, Depth, Fly, Weather, GPS,     |
        |  Setup Used, Strategy Deployed, Notes)           |
        +--------------------------------------------------+
```

---

## 2. Model Specifications

### A. `Strategy` Model
- **`name`** (`CharField`, max 150): Name of the strategy (e.g., *"Chironomid Wind Drift at 15ft"*, *"Leptophlebia Nymph Slow Crawl along Drop-off"*, *"Fast Strip Streamer in Shallows"*).
- **`setup`** (`ForeignKey` to `Setup`, `null=True, blank=True, on_delete=SET_NULL`): The line setup / rig configured for this strategy.
- **`author`** (`ForeignKey` to `User`, `on_delete=CASCADE`): Angler who created the strategy.
- **`notes`** (`CKEditor5Field`): In-depth strategy documentation (retrieval technique, depth control, hookset timing, drift speed, water condition notes).
- **Media**:
  - `pictures` (`ManyToManyField` to `Picture`)
  - `videos` (`ManyToManyField` to `Video`)
  - `articles` (`ManyToManyField` to `Article`)
- **Timestamps**: `created_at`, `updated_at`.

---

### B. Setup Visibility & Public Sharing
- **Shared Line Configurations**: Setups (fly line, connection knot, leader length, strike indicator position, and downstream tippet / dropper sections) are accessible across all anglers when creating a Strategy or logging a catch.
- **Personal Tackle Privacy**: Personal rod & reel selections remain tied to the creator's personal locker. When other anglers view or select a shared setup, they see the rig specs and can use their own rod/reel or clone the rig.
- **Optional Privacy Toggle**: An optional `is_private` boolean field (default: `False` / Public) if an angler specifically wants to keep a private competition rig hidden.

---

### C. Catch Log (`Log`) Integration
- Add two optional foreign keys to the `Log` model:
  - `setup`: `models.ForeignKey(Setup, null=True, blank=True, on_delete=models.SET_NULL)`
  - `strategy`: `models.ForeignKey(Strategy, null=True, blank=True, on_delete=models.SET_NULL)`

---

## 3. User Experience & UI Workflow

1. **Catch Log Detail (`log_detail.html` & catch cards)**:
   - Displays clear badges / pill links for **Strategy** and **Setup** used.
   - Clicking either link opens the full details (interactive rig diagram, strategy notes, videos/pictures).

2. **Smart Logging (`log_form.html` & Mobile Log)**:
   - Selecting a **Strategy** automatically pre-selects its default **Setup**.
   - Anglers can still change or customize the setup if they altered their rig on the water.
   - Both fields remain optional to keep fast catch logging friction-free.

3. **Strategy Management**:
   - Strategy List view with search, filter, and media counters.
   - Strategy Detail view with rich CKEditor notes, linked setup rig diagram, and media tabs (videos, articles, pictures).
   - Strategy Create/Edit form with same-screen quick-add setup selector.

---

## 4. Implementation Checklist

- [ ] Create `Strategy` model in `catches/models.py`.
- [ ] Add `setup` and `strategy` foreign keys to `Log` model in `catches/models.py`.
- [ ] Update `Setup` model visibility / sharing.
- [ ] Generate and apply database migrations.
- [ ] Create `Strategy` forms (`New_Strategy_Form`).
- [ ] Build Strategy views (`StrategyListView`, `StrategyDetailView`, `StrategyCreateView`, `StrategyUpdateView`, `StrategyDeleteView`).
- [ ] Add Strategy routes to `catches/urls.py`.
- [ ] Create Strategy templates:
  - `strategy_list.html`
  - `strategy_detail.html`
  - `strategy_form.html`
  - `strategy_confirm_delete.html`
- [ ] Update `log_form.html`, `log_detail.html`, and `mobile_log.html` / API to support Strategy and Setup selection.
- [ ] Add Strategy link to navbar and cross-navigation.
