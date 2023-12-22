

def collect_paths_recursive(start, path_map,
                            collected_paths, current_path=None):
    """
    Recursive depth-first iteration.
    @start: key to lookup in @path_map this iteration. Must support
            __eq__ and __hash__
    @path_map: dictionary in the form
               {start: [list of future @start elem],
                key: [list of future keys]}
    @collected_paths: list where all of the output paths will be put
    @current_path: a list that will hold the path as it is built.
    """
    # make an initial current_path if one doesn't exist
    if current_path is None:
        current_path = []

    next_paths = path_map.get(start)
    # end condition
    if next_paths is None or next_paths == [start]:
        current_path_copy = [i for i in current_path]
        # copy doesn't exist on py 2
        collected_paths.append([i for i in current_path])
        current_path.pop()
        return

    looked_up_paths = []
    for c in next_paths:
        # skip paths that would infinitely loop
        if c == start:
            continue
        current_path.append(c)
        collect_paths_recursive(c, path_map, collected_paths,
                                current_path)
    current_path.pop()
    return


