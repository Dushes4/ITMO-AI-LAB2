from collections import deque


def dfs(graph, used, x, target):
    used.append(x)

    if x == target:
        print("DFS: ", used)
        return

    for y in graph[x]:
        if y not in used:
            dfs(graph, used, y, target)


def bfs(graph, used, x, target):
    q = deque()
    for i in graph[x]:
        q.append(i)

    while q:
        x = q.popleft()
        if x not in used:
            used.append(x)
            if x != target:
                for i in graph[x]:
                    q.append(i)
            else:
                print("BFS: ", used)
                return
    return


def dfsl(graph, used, x, target, d, max_d, iterated):
    used.append(x)

    if x == target:
        if not iterated:
            print("DFSL: " + str(used))
        return True

    for y in graph[x]:
        if y not in used and d < max_d:
            if dfsl(graph, used, y, target, d + 1, max_d, iterated):
                return True
    return


def dfsli(graph, used, x, target, d, max_d):
    while not dfsl(graph, used, x, target, 1, d, True) and d <= max_d:
        print("DFSLI" + str(d) + ": " + str(used))
        used.clear()
        d += 1
    if d <= max_d:
        print("DFSLI" + str(d) + ": " + str(used))
    return


def bisearch(graph, start_used, finish_used, start, finish, max_d):
    d = 1
    while d < max_d:
        start_used = []
        finish_used = []
        start_res = dfsl(graph, start_used, start, finish, 1, d, True)
        finish_res = dfsl(graph, finish_used, finish, start, 1, d, True)

        mid = None
        for x in start_used:
            for y in finish_used:
                if x == y:
                    mid = x

        if mid is not None:
            print("BISEARCH - MID (" + str(mid) + "-" + str(d) + "):")
            print(start_used)
            print(finish_used)
            return
        elif start_res:
            print("BISEARCH - START (" + str(d) + "):")
            print(start_used)
            return
        elif finish_res:
            print("BISEARCH - FINISH (" + str(d) + "):")
            print(finish_used)
            return
        else:
            d *= 2
    return


def greedy_search(graph, used, x, finish, distance_to_nov):
    used.append(x)
    if x == finish:
        print("GREEDY SEARCH:")
        print(used)
        return

    distances = []
    for y in graph[x]:
        distances.append([distance_to_nov[y], y])
    distances.sort()

    for way in distances:
        if way[1] not in used:
            greedy_search(graph, used, way[1], finish, distance_to_nov)


def a_star_search(graph, graph_w, used, x, finish, distance_to_nov, cost):
    used.append(x)

    if x == finish:
        print("\nCOST: " + str(cost))
        print(used)
        return

    print(x, graph_w[x])
    best_y = None
    for y in graph[x]:
        if y not in used:
            print(graph_w[x][y] + distance_to_nov[y], y)
            if best_y == None or graph_w[x][y] + distance_to_nov[y] <= graph_w[x][best_y] + distance_to_nov[best_y]:
                best_y = y

    if best_y is not None:
        a_star_search(graph, graph_w, used, best_y, finish, distance_to_nov, cost + graph_w[x][best_y])


if __name__ == '__main__':
    distance_to_nov = {
        "Брест": 1389,
        "Вильнюс": 1185,
        "Витебск": 867,
        "Воронеж": 599,
        "Волгоград": 845,
        "Даугавпилс": 1078,
        "Донецк": 926,
        "Калининград": 1482,
        "Каунас": 1264,
        "Казань": 323,
        "Киев": 1099,
        "Житомир": 1214,
        "Кишинев": 1482,
        "Ниж.Новгород": 0,
        "С.Петербург": 893,
        "Самара": 527,
        "Симферополь": 1437,
        "Минск": 1073,
        "Москва": 397,
        "Мурманск": 1984,
        "Орел": 627,
        "Одесса": 1421,
        "Рига": 1211,
        "Таллин": 1183,
        "Уфа": 776,
        "Харьков": 868,
        "Ярославль": 287
    }

    graph = {}
    graph_w = {}
    used = []
    input_file = open("LAB2DATA.csv", "r", encoding="utf8")
    line = input_file.readline()
    while line != "":
        line = line.split(",")
        line[-1] = int(line[-1])
        if line[0] in graph:
            graph[line[0]].append(line[1])
            graph_w[line[0]][line[1]] = line[2]
        else:
            graph[line[0]] = [line[1]]
            graph_w[line[0]] = {line[1]: line[2]}
        if line[1] in graph:
            graph[line[1]].append(line[0])
            graph_w[line[1]][line[0]] = line[2]
        else:
            graph[line[1]] = [line[0]]
            graph_w[line[1]] = {line[0]: line[2]}

        line = input_file.readline()

    input_file.close()
    print(graph)
    print(graph_w)

    start = "Харьков"
    finish = "Ниж.Новгород"
    print('--------------------------------------------------')
    
    dfs(graph, used, start, finish)
    print('--------------------------------------------------')
    used.clear()

    bfs(graph, used, start, finish)
    print('--------------------------------------------------')
    used.clear()

    dfsl(graph, used, start, finish, 1, 8, False)
    print('--------------------------------------------------')
    used.clear()

    dfsli(graph, used, start, finish, 1, 8)
    print('--------------------------------------------------')
    used.clear()

    start_used = []
    finish_used = []
    bisearch(graph, start_used, finish_used, start, finish, 16)
    print('--------------------------------------------------')

    greedy_search(graph, used, start, finish, distance_to_nov)
    used.clear()

    print('--------------------------------------------------')
    print("A STAR SEARCH: ")
    a_star_search(graph, graph_w, used, start, finish, distance_to_nov, 0)
