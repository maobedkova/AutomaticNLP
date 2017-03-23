# Preprocessing: sub \r\n^[^\w<\|\(\[\]\)\-/\.,]+ in NotePad

import re

f = open('abr2w.txt', 'r', encoding='utf-8')
w = open('synonyms.tei', 'w', encoding='utf-8')
t = open('test_synonyms.txt', 'w', encoding='utf-8')

body = ''
num = 1

for line in f:
    print (line)
    t.write(line)

    ### REFERENCE
    reference = re.findall('[Сс]м\. ?([-\w\(\) ,.]+?) ?[.\n\|;]', line)
    ref_body = ''
    for ref in reference:
        refs = re.split(', ?', ref)
        ref_body = '<xr type="synonym">\n<lbl>Смотри синоним</lbl>\n'
        for ref in refs:
            ref_body += '<ref>' + ref + '</ref>\n'
        ref_body += '</xr>\n'
    new_line = re.sub('([Сс]м\. ?[-\w\(\) ,.]+?) ?(?:[.\n\|;])', '', line)

    if reference:
        print('REF', reference)
        t.write('REF ' + str(reference) + '\n')


    ### COMPARISON
    comparison = re.findall('\[?[Сс]р\. ?<?([^><\]\[]+)>?\]?', new_line)
    comp_body = ''
    for c in comparison:
        comps = re.split(' и |, ?', c)
        comp_body = '<xr type="synonym">\n<lbl>Сравни с</lbl>\n'
        for comp in comps:
            comp_body += '<ref>'+comp+'</ref>\n'
        comp_body += '</xr>\n'
    new_line = re.sub('\[?[Сс]р\. ?<?([^><\]\[]+)>?\]?', '', new_line)

    if comparison:
        print('COMP', comparison)
        t.write('COMP ' + str(comparison) + '\n')


    ### ANTONYM
    antonym = re.findall('[Пп]рот\. ?<(.+?)>', new_line)
    ant_body = ''
    for a in antonym:
        ants = re.split(' и |, ?', a)
        ant_body = '<xr type="antonym">\n<lbl>\nПротивопоставление с</lbl>\n'
        for ant in ants:
            ant_body += '<ref>' + re.sub('[><]', '', ant) + '</ref>\n'
        ant_body += '</xr>\n'
    new_line = re.sub('[Пп]рот\. ?<.+?>', '', new_line)

    if antonym:
        print('ANT', antonym)
        t.write('ANT ' + str(antonym) + '\n')


    ### DEFENITION
    defenition = re.findall('\[(.+?)(?:\(([\w., ]+?)\))?\]', new_line)
    def_body= ''
    for defen in defenition:
        def_body += '<def>\n<text>'+re.sub('[><]', '', defen[0])+\
                    '</text>\n<ref>'+defen[1]+'</ref>\n</def>\n'
    new_line = re.sub('\[(.+?)(?:\(([\w., ]+?)\))?\]', '', new_line)

    if defenition:
        print ('DEF', defenition)
        t.write('DEF ' + str(defenition) + '\n')


    ### IDIOM
    idioms = re.findall('\|+ ?([-\w\(\) ,.?!;]+?) ?(?:\n|[Сс]м\.)', new_line)
    new_line = re.sub('\|+ ?[-\w\(\) ,.?!;]+? ?(?:\n|[Сс]м\.)', '', new_line)
    id_body = ''
    for idiom in idioms:
        ids = re.split(', ?', idiom)
        for id in ids:
            id_body += '<text>' + re.sub('[><]', '', id) + '</text>\n'
    if id_body != '':
        id_body = '<cit type="colloc">\n<form><usg type="style">Идиома</usg></form>' + id_body + '</cit>\n'

    if idioms:
        print('ID', idioms)
        t.write('ID ' + str(idioms) + '\n')


    ### FORM
    forms1 = re.findall('^[-\w .!]+\(([-\w .,]+?)\)', new_line)
    new_line = re.sub('\([-\w .,]+?\)', '', new_line)
    forms2 = re.findall('((?:Действ|Страд)\. форма): <(.+?)>', new_line)
    new_line = re.sub('((?:Действ|Страд)\. форма): <(.+?)>', '', new_line)
    forms = forms1 + forms2
    sex_body = ''
    asp_body = ''
    part_body = ''
    form_body = ''
    for f in forms1:
        if re.search('^\w\. \w\. .+', f):
            sex_body += '<cit type="gender_parallel">'+f+'</cit>\n'
        elif re.search('^-|-$', f):
            part_body += '<orth extent="part">'+f+'</orth>\n'
        else:
            part_body += '<orth>'+f+'</orth>\n'

    for f in forms2:
        asp_body += '<orth>' + f[1] + '</orth>\n<note>' +f[0]+ '</note>\n'

    if asp_body != '':
        asp_body = '<inflection>\n' + asp_body + '</inflection>\n'
    if part_body != '':
        part_body = '<inflection>\n' + part_body + '</inflection>\n'
    if asp_body != '' or part_body != '':
        form_body += '<form type="inflected">\n' + asp_body + part_body + '</form>\n'

    if forms:
        print('FOR', forms)
        t.write('FOR ' + str(forms) + '\n')


    ### EXAMPLE
    examples = []
    examples1 = re.findall('\. ?([А-Я][^.]+?(?:\.\.\.)?)[\">]\.? ?(.+?)\.', new_line)
    new_line = re.sub('\. ?([А-Я][^.]+?(\.\.\.)?)[\">]\.? ?(.+?)\.', '', new_line)
    examples2 = re.findall('// ?([^\">]+?)\. ?(.+?)\.', new_line)
    new_line = re.sub('// ?[^\">]+?\. ?.+?\.', '', new_line)
    examples3 = re.findall('[\"<](.+?)[\">]\.? ?(.+?)\.', new_line)
    new_line = re.sub('[\"<](.+?)[\">]\.? ?(.+?)\.', '', new_line)
    examples += examples1 + examples2 + examples3
    ex_body = ''
    for ex in examples:
        if re.search('\w', ex[0]):
            ex_body += '<cit type="example">\n<text>'+re.sub('[><]', '', ex[0])+\
                       '</text>\n<ref>'+re.sub('[><]', '', ex[1])+'</ref>\n</cit>\n'
        else:
            ex_body += '<cit type="example">\n<text>' + re.sub('[><]', '', ex[0]) + '</text>\n</cit>\n'
    examples4 = re.findall('<(.+?)>\.', new_line)
    new_line = re.sub('<(.+?)>\.', '', new_line)
    if examples4:
        ex_body += '<cit type="example">\n<text>'+re.sub('[><]', '', examples4[0])+'</text>\n</cit>\n'

    if examples or examples4:
        print ('EX', examples + examples4)
        t.write('EX ' + str(examples + examples4) + '\n')

    ### SYNONYM
    syn_contexts = re.findall('([-\w\(\) .!]*?)[;,:] ?(.+?)$', new_line)
    cont_body = ''
    syns = []
    for context in syn_contexts:
        contexts = re.split('[;.]', syn_contexts[0][1])
        for cont in contexts:
            cont = re.sub('(^ +|[. ]+$)', '', cont)
            if ',' in cont:
                cont_body += '<set>'+re.sub(' *, *', ', ', re.sub('[^-\w, ]', '', cont))+'</set>\n'
            elif ' ' in cont:
                syns.append(cont)
    if cont_body != '':
        cont_body = '<xr type="synonym">\n' + cont_body + '</xr>\n'

    syn_body = ''
    for syn in syns:
        syn_body += '<ref>'+re.sub('[><]', '', syn)+'</ref>\n'
    if syn_body != '':
        syn_body = '<xr type="synonym">'+syn_body+'</xr>\n'

    new_line = re.sub('[;,:] ?(.+?)$', '', new_line)

    if syn_contexts:
        print('CON', syn_contexts)
        t.write('CON ' + str(syn_contexts) + '\n')

    ### WORD
    input = re.findall('[-\w !.]+', new_line)
    word_body = ''
    if input != []:
        word = re.sub(' +$', '', input[0])
        word_body += '<entry type="main">\n<index>'+str(num)+\
                     '</index>\n<symbol>'+word[0]+'</symbol>\n<form>\n<orth type="lemma" extent="full">'+word+'</orth>\n</form>\n'
    new_line = re.sub('[-\w !.]+', '', new_line)

    print ('W', word)
    t.write('W ' + str(word) + '\n')

    print ('='*30)
    t.write('='*30 + '\n')

    num += 1

    body += word_body + \
              form_body + \
              '<sense n="1">\n' + \
              def_body + \
              ex_body + \
              id_body + \
              sex_body + \
              '</sense>\n' + \
              comp_body + \
              ref_body + \
              cont_body + \
              syn_body + \
              ant_body + \
              '</entry>\n'


header = '<xml>\n' \
         '<fileDesc>\n' \
         '<respStmt>\n' \
         '<name>Мария Объедкова</name>\n' \
         '</respStmt>\n' \
         '<extent>19108</extent>\n' \
         '<sourceDesc>\n' \
         '<ref target="http://www.cdmail.ru/literature/dictionaries/slovar-sinonimov.htm"></ref>\n' \
         '<p>This database was converted from the Russian Synonym Dictionary.</p>\n' \
         '</sourceDesc>\n' \
         '</fileDesc>\n' \
         '<front>\n' \
         '<head>\n' \
         '<title dict_id="">Словарь русских синонимов и сходных по смыслу выражений</title>\n' \
         '<author>Наум Абрамович Переферкович</author>\n' \
         '<pubdate>1900</pubdate>\n' \
         '<language type="content">\n' \
         '<idno type="iso639-3">rus</idno>\n' \
         '</language>\n' \
         '</head>\n' \
         '</front>\n' \
         '<body>\n' \
         '<div>\n' \
         '<superEntry>\n'

footer = '</superEntry>\n' \
         '</div>\n' \
         '</body>\n' \
         '</xml>\n'

main = header + body + footer
w.write(main)

