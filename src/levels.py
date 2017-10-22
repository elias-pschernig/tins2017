import game

class Level:
    int number
    int tick
    int tools[10]
    str name
    int required
    bool done

Level level

def squared_forest(int xr, yr, trees, good):
    for int i in range(trees):
        str kinds[] = {"oak", "fir", "eucalypt"}
        int rk = 2
        if i < good:
            rk = land_rand(0, 1)
        str kind = kinds[rk]
        for int r in range(100):
            float x = land_rnd(-xr, xr)
            float y = land_rnd(-yr, yr)

            Tree *tree = place_tree(x, y, kind)
            if tree: break

def round_forest(int radius, trees, good):
    for int i in range(trees):
        str kinds[] = {"oak", "fir", "eucalypt"}
        int rk = 2
        if i < good:
            rk = land_rand(0, 1)
        str kind = kinds[rk]
        for int r in range(100):
            float a = land_rnd(-pi, pi)
            float d = land_rnd(0, radius)
            float x = d * cos(a)
            float y = d * sin(a)
            Tree *tree = place_tree(x, y, kind)
            if tree: break

def tools(int water, wind, fire, oaks, firs):
    level.tools[0] = water
    level.tools[1] = wind
    level.tools[2] = fire
    level.tools[3] = oaks
    level.tools[4] = firs

def levels_start(int number) -> Level*:
    level.number = number
    level.tick = 0
    level.done = False

    level.name = "the end"
    tools(-1, -1, -1, -1, -1)

    if number == 1:
        squared_forest(100, 100, 20, 20)
        level.required = 15
        tools(150, 0, 0, 0, 0)
        level.name = "Use your Bog-Douser™!"

    if number == 2:
        squared_forest(400, 50, 30, 30)
        level.required = 15
        tools(100, 0, 0, 0, 0)
        level.name = "Douse the forest fires!"

    if number == 3:
        squared_forest(150, 150, 30, 30)
        level.required = 20
        tools(50, 100, 0, 0, 0)
        level.name = "Beetles again! Use the Tree-Tosser™!"

    if number == 4:
        round_forest(200, 40, 40)
        level.required = 30
        tools(200, 200, 0, 0, 0)
        level.name = "Protect the forest!"

    if number == 5:
        round_forest(400, 31, 30)
        level.required = 10
        tools(0, 0, 100, 0, 0)
        level.name = "Invasive species! Use the Flame-Thrower™!"

    if number == 6:
        round_forest(70, 10, 10)
        level.required = 10
        tools(0, 0, 200, 0, 0)
        level.name = "Kill them with fire!"

    if number == 7:
        round_forest(400, 50, 45)
        level.required = 30
        tools(100, 100, 100, 0, 0)
        level.name = "Pest control..."

    if number == 8:
        level.required = 20
        tools(0, 0, 200, 100, 0)
        level.name = "Reforestation"

    if number == 9:
        level.required = 20
        tools(0, 0, 900, 0, 100)
        level.name = "Reforestation part 2"

    if number == 10:
        level.required = 60
        round_forest(400, 100, 95)
        tools(999, 999, 999, 50, 50)
        level.name = "Plagued!"

    if number == 11:
        level.required = 30
        round_forest(400, 100, 50)
        tools(999, 999, 999, 50, 50)
        level.name = "Overgrown!"

    if number == 12:
        level.required = 30
        round_forest(400, 100, 95)
        tools(999, 999, 999, 10, 10)
        level.name = "The final test"
    
    return &level

def beetles(int n, radius):
    for int i in range(n):
        float a = land_rnd(0, 2 * pi)
        float x = radius * cos(a)
        float y = radius * sin(a)
        place_tree(x, y, "beetle")

def fires(int n, radius):
    for int i in range(n):
        float a = land_rnd(0, 2 * pi)
        float x = radius * cos(a)
        float y = radius * sin(a)
        place_tree(x, y, "fir")
        trees_callback(game.trees, x, y, 30, tree_burn)

def levels_tick:
    level.tick++
    if level.number == 1:
        for int wave in range(10):
            if level.tick == 180 + 180 * wave:
                if wave < 4: beetles(1, 400)
                elif wave < 8: beetles(2, 400)
                elif wave < 9: beetles(3, 400)
                else:
                    beetles(4, 400)
                    level.done = True

    if level.number == 2:
        for int wave in range(3):
            if level.tick == 180 + 240 * wave:
                if wave == 2:
                    level.done = True
                place_tree(-400, 0, "fir")
                trees_callback(game.trees, -400, 0, 30, tree_burn)
                place_tree(400, 0, "fir")
                trees_callback(game.trees, 400, 0, 30, tree_burn)

                if wave == 2:
                    place_tree(0, 0, "fir")
                    trees_callback(game.trees, 0, 0, 30, tree_burn)

    if level.number == 3:
        for int wave in range(10):
            if level.tick == 180 + 180 * wave:
                if wave < 4: beetles(2, 400)
                elif wave < 8: beetles(3, 400)
                elif wave == 8: beetles(4, 400)
                elif wave == 9:
                    beetles(5, 400)
                    level.done = True

    if level.number == 4:
        for int wave in range(14):
            if level.tick == 180 + 180 * wave:
                if wave % 2 == 0:
                    beetles(1, 400)
                else:
                    fires(1, 200)
                if wave == 13:
                    level.done = True

    if level.number == 5:
        for int wave in range(1):
            if level.tick == 180 + 180 * wave:
                level.done = True

    if level.number == 6:
        for int wave in range(10):
            if level.tick == 180 + 180 * wave:
                if wave < 4: beetles(1, 400)
                elif wave < 8: beetles(2, 400)
                elif wave < 9: beetles(3, 400)
                else:
                    beetles(4, 400)
                    level.done = True

    if level.number == 7:
        for int wave in range(8):
            if level.tick == 180 + 180 * wave:
                beetles(2, 400)
                if wave == 7:
                    level.done = True

    if level.number == 8:
        for int wave in range(1):
            if level.tick == 180 + 180 * wave:
                level.done = True

    if level.number == 9:
        for int wave in range(1):
            if level.tick == 180 + 180 * wave:
                level.done = True

    if level.number == 10:
        for int wave in range(7):
            if level.tick == 180 + 180 * wave:
                beetles(1 + wave, 450)
                if wave == 6:
                    level.done = True

    if level.number == 11:
        for int wave in range(6):
            if level.tick == 180 + 180 * wave:
                fires(1 + wave, 450)
                if wave == 5:
                    level.done = True

    if level.number == 12:
        for int wave in range(20):
            if level.tick == 180 + 180 * wave:
                if wave % 4 == 0:
                    beetles(2, 450)
                if wave % 4 == 1:
                    beetles(3, 450)
                if wave % 4 == 2:
                    fires(2, 400)
                if wave % 4 == 3:
                    fires(1, 400)
                    beetles(1, 400)
                    place_tree_rising(land_rnd(-400, 400), land_rnd(-400, 400), "eucalypt", True)
                if wave == 19:
                    level.done = True
