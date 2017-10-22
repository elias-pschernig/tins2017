import game

def levels_start(int number):
    int trees = 100
    int good = 50
    int confined = 480

    if number == 1:
        trees = 20
        good = 20
        confined = 100
        Tree *beetle = place_tree(-400, 0, "beetle")
        beetle.beetle = True
    
    for int i in range(trees):
        str kinds[] = {"oak", "fir", "eucalypt"}
        int rk = 2
        if i < good:
            rk = land_rand(0, 1)
        str kind = kinds[rk]
        for int r in range(100):
            float x = land_rnd(-confined, confined)
            float y = land_rnd(-confined, confined)

            Tree *tree = place_tree(x, y, kind)
            if tree: break
