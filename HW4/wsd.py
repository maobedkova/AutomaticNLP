from nltk.corpus import wordnet
from nltk.wsd import lesk

# 1) Найти все значения (синсеты) для лексемы plant
for synset in wordnet.synsets('plant'):
  print(synset, synset.definition())

print('~'*20)

# 2) Найти определение для лексемы plant в значении (а) "завод" и в значении (b) "растение"
print("завод:", wordnet.synset('plant.n.01'), wordnet.synset('plant.n.01').definition())
print("растение:", wordnet.synset('plant.n.02'), wordnet.synset('plant.n.02').definition())

print('~'*20)

# 3) Найдите два произвольных контекста для слова plant в значениях (a) "завод" и (b) "растение";
# продемонстрируйте на них действие алгоритма Леска для разрешения неоднозначности

print('Первый контекст:', lesk('If a plant cannot live according to its nature, it dies'.split(), 'plant', 'n').definition())
print('Второй контекст:', lesk('Previous experience working in a chemical plant is preferred'.split(), 'plant', 'n').definition())

print('~'*20)

# 4) Найдите гиперонимы для значения (a) и гиперонимы для значения (b)

print('Гиперонимы к "завод":')
for hyp in wordnet.synset('plant.n.01').hypernyms():
    print(hyp, hyp.definition())

print ('Гиперонимы к "растение":')
for hyp in wordnet.synset('plant.n.02').hypernyms():
    print(hyp, hyp.definition())

print('~'*20)

# 5) Вычислите наименьшее расстояние между значением plant "завод" и значениями лексемы industry,
# а также plant "растение" и значениями лексемы leaf
# Найти min (d(plant: "завод", industry), d(plant: "завод", leaf)),
# а также min (d(plant: "растение", industry), d(plant: "растение", leaf))

# synset1.path_similarity(synset2): based on the shortest path that connects the senses in the is-a (hypernym/hypnoym) taxonomy]

industry_plant1 = [wordnet.synset('plant.n.01').path_similarity(s) for s in (wordnet.synsets('industry'))]
leaf_plant1 = [wordnet.synset('plant.n.01').path_similarity(s) for s in (wordnet.synsets('leaf'))]
print ('Минимальное расстояние между "завод" и industry:', min(min(industry_plant1), min(value for value in leaf_plant1 if value is not None)))

leaf_plant2 = [wordnet.synset('plant.n.02').path_similarity(s) for s in (wordnet.synsets('leaf'))]
industry_plant2 = [wordnet.synset('plant.n.02').path_similarity(s) for s in (wordnet.synsets('industry'))]
print ('Минимальное расстояние между "растение" и leaf:', min(min(value for value in leaf_plant2 if value is not None), min(industry_plant2)))

print('~'*20)

# 6)Вычислить двумя разными способами расстояние:
# d(plant: "растение", rattlesnake's master) и d(organism, whole)
# Есть ли разница в расстояниях?
# Какое из расстояний, по Вашему мнению, в лучшей степени отражает интуитивное представление о семантчиеской близости слов?

# Leacock-Chodorow Similarity: Return a score denoting how similar two word senses are,
# based on the shortest path that connects the senses (as above) and the maximum depth of the taxonomy
# in which the senses occur. The relationship is given as -log(p/2d) where p is the shortest path length and d the taxonomy depth.

plant_rattle_lch = [wordnet.synset('plant.n.02').lch_similarity(s) for s in (wordnet.synsets('rattlesnake_master'))]
print ('Расстояние lch между "растение" и rattlesnake`s master:', min(plant_rattle_lch))

organism_whole_lch = []
for w_s in (wordnet.synsets('organism')):
    organism_whole_lch += [o_s.lch_similarity(w_s) for o_s in (wordnet.synsets('organism'))]
print ('Расстояние lch между organism и whole:', min(organism_whole_lch))

# Wu-Palmer Similarity: Return a score denoting how similar two word senses are,
# based on the depth of the two senses in the taxonomy and that of their Least Common Subsumer (most specific ancestor node).
# Note that at this time the scores given do _not_ always agree with those given by
# Pedersen's Perl implementation of Wordnet Similarity.

plant_rattle_wup = [wordnet.synset('plant.n.02').lch_similarity(s) for s in (wordnet.synsets('rattlesnake_master'))]
print ('Расстояние wup между "растение" и rattlesnake`s master:', min(plant_rattle_wup))

organism_whole_wup = []
for w_s in (wordnet.synsets('organism')):
    organism_whole_wup += [o_s.wup_similarity(w_s) for o_s in (wordnet.synsets('organism'))]
print('Расстояние wup между organism и whole:', min(organism_whole_lch))

# Расстояние не отличается.
