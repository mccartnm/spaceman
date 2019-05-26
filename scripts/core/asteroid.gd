extends StaticBody2D

var _health = 400;

func hit(damage):
    _health -= damage;

    if _health <= 0:
        print ("crumble!")
        queue_free();

func _ready():
    pass
