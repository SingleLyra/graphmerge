# node type:
class Node(object):
    def __init__(self, value:int, l, r, cost, sorted_id = 0):
        self.value = value
        self.l = l
        self.r = r
        self.cost = cost
        self.sorted_id = sorted_id

def SortL(node:Node):
    return node.l

'''
def find_fa(x, merged, node_sorted):
   if x == merged[x]:
        return x
    node_sorted[merged[x]].cost += node_sorted[x].cost
    node_sorted[x].cost = 0
    merged[x] = find_fa(merged[x], merged, node_sorted)
    return merged[x]
def merge(x, y, merged, node_sorted): # merge x into y.
    print("merge: {} {}".format(x, y))
    #merged[x] = find_fa(y, merged, node_sorted)
    #node_sorted[merged[x]].cost += node_sorted[x].cost
    #node_sorted[x].cost = 0
    print("merge end: {} {}".format(merged[x], x))
'''


def Graph_merge(n:int, hash_map:dict, node_list:list):
    # input: n: number of vertices; hash_map: key : (i, j) for all edges; node_list: for all nodes.
    # output: new dict, for the rebuild graph.

    # Step 1 start.
    node_sorted = node_list.copy()
    node_sorted.sort(key = SortL)
    Id2Sorted = {}
    for i in range(n):
        Id2Sorted[node_sorted[i].value] = i
        node_sorted[i].sorted_id = i
    now_set, belong_set = 0, [[node_sorted[0],],]
    now_set_r = node_sorted[0].r
    for i in range(n):
        if i == 0:
            continue
        if node_sorted[i].l <= now_set_r:
            belong_set[now_set].append(node_sorted[i])
        else:
            now_set = now_set + 1
            now_set_r = 0
            belong_set.append([node_sorted[i],])
        now_set_r = max(now_set_r, node_sorted[i].r)
    # Step 1 end.

    # Step 2 begin.
    bel_step2, cost = {}, {}
    set_step2 = []
    for setid in range(len(belong_set)):
        cluster = belong_set[setid]
        set_count = 0
        set_step2.append([])
        for _, vi in enumerate(cluster):
            bitset = []
            for __ in range(_):
                bitset.append(True)
            merge_front = False
            for __ in range(_):
                vj = cluster[__]
                # print(vi, vj)
                if bitset[__] == False:
                    continue
                if merge_front == True:
                    break
                if (vi.value, vj.value) not in hash_map: # try to merge i into j.
                    merge_flag = True
                    print("?",bel_step2[vj.sorted_id],"REVEDGE:",vi.value,vj.value)
                    for vk in set_step2[setid][bel_step2[vj.sorted_id]]:
                        if (vk.value, vi.value) in hash_map:
                            merge_flag = False # if merge i into j, will cause self-loop
                    if merge_flag == True:
                        bel_step2[vi.sorted_id] = bel_step2[vj.sorted_id]
                        set_step2[setid][bel_step2[vi.sorted_id]].append(vi)
                        cost[bel_step2[vi.sorted_id]] += vi.cost
                        merge_front = True
                    else:
                        for vk in set_step2[setid][bel_step2[vj.sorted_id]]: # Merge i into j is impossible, then merge i into every element in set[j] is impossible.
                                bitset[vk.sorted_id] = False

            if merge_front == False: # all nodes can't fulfill merge condition, then add a new set.
                set_count = set_count + 1
                bel_step2[vi.sorted_id] = set_count - 1
                set_step2[setid].append([vi, ])
                cost[bel_step2[vi.sorted_id]] = vi.cost
    # Step 2 end.
    # Build new graph.
    new_dict = {}
    for key in hash_map:
        a, b = (bel_step2[Id2Sorted[key[0]]], bel_step2[Id2Sorted[key[1]]])
        print("edge_new:",a,b,"edge_org",key[0],key[1])
        new_dict[(a, b)] = True
    for i in range(n):
        node_list[node_sorted[i].value].cost = cost[bel_step2[i]]
    # Build new graph end.
    return new_dict.copy()

if __name__ == '__main__':
    with open("n=500.txt", "r") as f:
        n, m = map(int, f.readline().split())
        hash_map = {}
        node_list = []
        for i in range(n):
            value = i
            l, r, cost = map(int, f.readline().split())
            node_list.append(Node(value,l,r,cost))
        for i in range(m):
            x, y = map(int, f.readline().split())
            hash_map[(x,y)] = True
            hash_map[(y,x)] = True
            # print(x, y)
        new_graph = Graph_merge(n,hash_map,node_list)
        for keys in new_graph.keys():
            print("new_graph:",keys[0], keys[1])
        for node in node_list:
            print("!",node.cost)