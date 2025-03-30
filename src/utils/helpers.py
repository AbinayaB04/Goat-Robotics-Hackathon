import heapq
def a_star_pathfinding(start, goal, vertices, neighbors):
    if start == goal:
        return [start]  # Return the current position as the path

    def heuristic(v1, v2):
        x1, y1 = vertices[v1][:2]
        x2, y2 = vertices[v2][:2]
        return abs(x1 - x2) + abs(y1 - y2)

    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in neighbors[current]:
            tentative_g_score = g_score[current] + heuristic(current, neighbor)
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                heapq.heappush(open_set, (tentative_g_score, neighbor))
                came_from[neighbor] = current

    return []  # Return an empty path if no valid path is found
