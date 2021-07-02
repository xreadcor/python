summa = 0
try:
path = nx.dijkstra_path(G, start, end)
if path != None:
for i in range(len(path) - 1):
summa += G[path[i]][path[i + 1]]['weight']

self.label_3.setVisible(True)
self.len_path.setText(str(summa))
self.error_msg.setText('Кратчайший путь: ' + str(path))

except:
self.error_msg.setText('Нет пути')