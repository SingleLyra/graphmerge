# 图合并算法简介：

## 算法原理

输入&输出：输入一个负载图，输出压缩后的负载图。

每个节点有自己的标号(value)，起始和终止时间(l&r)，负载(cost)。

## 压缩算法：

第一步：将每个节点按照时间的左端点(l)进行排序，并保存排序后的id，记为sorted_id. 然后对节点进行聚类，**聚类**方法为：如果a和b在时间上有重合，那么会将a和b合并。

第二步：对于每个类中的类内节点，按照排序后的点进行扫描，划分**新集合**。对于点$i$，如果能找到类内的前面某个点$j$，使得$i$到$j$没有边，同时$j$所在的**新集合**里面的所有的点$k$都和$i$没有连边，则把$i$加入到$j$所在的集合中。如果找不到这样一个$j$，则**新开一个集合**保存点$i$.'

最终压缩算法：对于第二步的每个集合，原图中的(a, b)变成了(set(a), set(b))。注意此时图中不应该有自环，有自环铁错。

## 算法代码：

#### 输入部分：

```python
    with open("n=500.txt", "r") as f:
        n, m = map(int, f.readline().split()) # 读入 点数, 边数
        hash_map = {} # 保存读入的边
        node_list = [] # 保存每个节点
        for i in range(n):
            value = i
            l, r, cost = map(int, f.readline().split()) # n行， 读入 l, r, cost. 皆为整数 
            node_list.append(Node(value,l,r,cost)) 
        for i in range(m):
            x, y = map(int, f.readline().split()) # 读入 x, y 代表 x, y的连边。
            hash_map[(x,y)] = True
            hash_map[(y,x)] = True
        new_graph = Graph_merge(n,hash_map,node_list) # 返回新图
```

#### 代码原理部分(第一步)：

```python
def Graph_merge(n:int, hash_map:dict, node_list:list):
    # input: n: number of vertices; hash_map: key : (i, j) for all edges; node_list: for all nodes.
    # output: new dict, for the rebuild graph.

    # Step 1 start.
    node_sorted = node_list.copy()
    node_sorted.sort(key = SortL) # 按照左端点排序
    Id2Sorted = {} # 节点原序号和排序后的序号映射
    for i in range(n):
        Id2Sorted[node_sorted[i].value] = i
        node_sorted[i].sorted_id = i
    now_set, belong_set = 0, [[node_sorted[0],],] # now_set 维护当前类的个数; belong_set[i]表示第i个类里面的所有节点
    now_set_r = node_sorted[0].r  # node_set_r 维护当前类内最大r
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
```

代码原理部分(第二步):

```python
def Graph_merge(n:int, hash_map:dict, node_list:list):
    # Step 1 ... #
    # Step 2 begin. 
    bel_step2, cost = {}, {} # bel_step 在step2中，每个点属于哪个新集合; cost:每个新集合的cost. 
    set_step2 = [] # set_step2[i]表示在第i个集合里面的每个点的列表。
    for setid in range(len(belong_set)): # 枚举类
        cluster = belong_set[setid] 
        set_count = 0
        set_step2.append([])
        for _, vi in enumerate(cluster): # 枚举类内点i
            bitset = [] # bitset维护当前确认到哪个节点，用于去掉非法的点j
            for __ in range(_):
                bitset.append(True)
            merge_front = False # merge_front用于找到j后及时退出
            for __ in range(_): # 枚举可能的点j
                vj = cluster[__]
                # print(vi, vj)
                if bitset[__] == False: # 如果当前点j已经不可行
                    continue
                if merge_front == True: # 如果当前已经找到了点j
                    break
                if (vi.value, vj.value) not in hash_map: # try to merge i into j.
                    merge_flag = True
                    print("?",bel_step2[vj.sorted_id],"REVEDGE:",vi.value,vj.value)
                    for vk in set_step2[setid][bel_step2[vj.sorted_id]]: # 如果找到了一个看起来可行的点j, 就枚举j所在集合的点k，查看是否和i有边
                        if (vk.value, vi.value) in hash_map:
                            merge_flag = False # if merge i into j, will cause self-loop
                    if merge_flag == True: # 如果j所在的集合都和i没有边
                        bel_step2[vi.sorted_id] = bel_step2[vj.sorted_id]
                        set_step2[setid][bel_step2[vi.sorted_id]].append(vi)
                        cost[bel_step2[vi.sorted_id]] += vi.cost
                        merge_front = True
                    else: # 否则就都把他们标成非法
                        for vk in set_step2[setid][bel_step2[vj.sorted_id]]: # Merge i into j is impossible, then merge i into every element in set[j] is impossible.
                                bitset[vk.sorted_id] = False

            if merge_front == False: # all nodes can't fulfill merge condition, then add a new set.
                set_count = set_count + 1
                bel_step2[vi.sorted_id] = set_count - 1
                set_step2[setid].append([vi, ])
                cost[bel_step2[vi.sorted_id]] = vi.cost
    # Step 2 end.
```

#### 代码原理部分(重建图)：

```python
def Graph_merge(n:int, hash_map:dict, node_list:list):
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
```

