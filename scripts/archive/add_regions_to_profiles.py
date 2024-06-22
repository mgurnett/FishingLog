from catches.models import Profile, Region


def run():
    profiles = Profile.objects.all()
    for p in profiles:
        print (f'{p = }')
        region = Region (
            name = "Favorite",
            notes = "Your personal favorite lakes",
            profile = p
        )
        print (f'{region = } {region.name = } {region.notes = }')
        region.save()