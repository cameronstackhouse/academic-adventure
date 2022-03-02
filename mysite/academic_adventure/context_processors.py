from .models import Event, CustomUser

def sidebar(request):
    """View displaying leaderboards to show a user their stats vs other people
    across campus"""
    gamekeeper = request.user.gamekeeper
    context = {"gamekeeper": gamekeeper,
            "scoreusers":sorted(CustomUser.objects.all(), key=lambda u:u.score, reverse = True)[:10],
            "intusers":sorted(CustomUser.objects.all(), key=lambda u:u.intelligence, reverse = True)[:5],
            "socusers":sorted(CustomUser.objects.all(), key=lambda u:u.sociability, reverse = True)[:5],
            "athusers":sorted(CustomUser.objects.all(), key=lambda u:u.athleticism, reverse = True)[:5]
            }
    return context