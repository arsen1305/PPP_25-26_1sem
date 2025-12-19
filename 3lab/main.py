graph = {
    'A': {'B': 3, 'C': 1},
    'B': {'A': 3, 'D': 5, 'E': 2},
    'C': {'A': 1, 'F': 4},
    'D': {'B': 5, 'G': 1},
    'E': {'B': 2, 'G': 3},
    'F': {'C': 4, 'G': 2},
    'G': {'D': 1, 'E': 3, 'F': 2}
}

log = []

def search_path(start, target, seen=None, path=None, dist=0):
    if seen is None:
        seen = set()
    if path is None:
        path = []
    
    path = path + [start]
    seen = seen.copy()
    seen.add(start)
    
    record = {
        'step': len(log) + 1,
        'vertex': start,
        'route': path.copy(),
        'distance': dist,
        'attempts': [],
        'best_from_here': None
    }
    
    if start == target:
        record['best_from_here'] = dist
        log.append(record)
        return dist, path
    
    min_dist = float('inf')
    shortest = None
    
    for next_v, cost in graph[start].items():
        if next_v in seen:
            continue
        
        record['attempts'].append({
            'to': next_v,
            'cost': cost,
            'new_dist': dist + cost
        })
        
        found_dist, found_path = search_path(
            next_v, target, seen, path, dist + cost
        )
        
        if found_dist < min_dist:
            min_dist = found_dist
            shortest = found_path
    
    record['best_from_here'] = min_dist
    log.append(record)
    
    if min_dist == float('inf'):
        return float('inf'), None
    return min_dist, shortest

def show_log():
    print('=' * 50)
    print('Поиск пути в графе')
    print('=' * 50)
    
    for entry in log:
        print(f"\nШаг {entry['step']}:")
        print(f"  Вершина: {entry['vertex']}")
        print(f"  Маршрут: {'->'.join(entry['route'])}")
        print(f"  Пройдено: {entry['distance']}")
        
        if entry['attempts']:
            print('  Варианты:')
            for a in entry['attempts']:
                print(f"    {entry['vertex']}->{a['to']} (вес:{a['cost']}, будет:{a['new_dist']})")
        
        if entry['best_from_here'] is not None:
            if entry['best_from_here'] == float('inf'):
                print('  До цели: ∞')
            else:
                print(f"  До цели: {entry['best_from_here']}")
    
    print('\n' + '=' * 50)

if __name__ == '__main__':
    print('Граф:')
    for v, n in graph.items():
        print(f'  {v}: {n}')
    
    print('\nВершины: A, B, C, D, E, F, G')
    
    from_v = input('Откуда: ').upper()
    to_v = input('Куда: ').upper()
    
    if from_v not in graph:
        print(f'Нет вершины {from_v}!')
    elif to_v not in graph:
        print(f'Нет вершины {to_v}!')
    else:
        log.clear()
        print(f'\nПоиск {from_v} -> {to_v}...')
        
        length, route = search_path(from_v, to_v)
        
        show_log()
        
        print('\nИтог:')
        if length == float('inf'):
            print(f'Нет пути {from_v} -> {to_v}!')
        else:
            print(f'Кратчайший: {"->".join(route)}')
            print(f'Длина: {length}')
