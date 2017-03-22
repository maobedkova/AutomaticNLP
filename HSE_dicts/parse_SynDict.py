# Preprocessing: sub \r\n^[^\w<\|\(\[\]\)\-/\.,]+ in NotePad

import re

f = open('abr2w.txt', 'r', encoding='utf-8')
w = open('test.xml', 'w', encoding='utf-8')

body = ''

for line in f:
    # w.write(line + '\n')
    print (line)

    ### REFERENCE
    reference = re.findall('[Сс]м\. ?([-\w\(\) ,.]+?) ?[.\n\|;]', line)
    ref_body = ''
    for ref in reference:
        refs = re.split(', ?', ref)
        ref_body = '<xr type="syn">\n<lbl>Смотри синоним</lbl>\n'
        i = 1
        for ref in refs:
            ref_body += '<ref n="' + str(i) + '">\n' + ref + '</ref>\n'
            i += 1
        ref_body += '</xr>\n'

    # w.write('R' + ref_body + '\n')
    print('REF', refs)

    new_line = re.sub('([Сс]м\. ?[-\w\(\) ,.]+?) ?(?:[.\n\|;])', '', line)


    ### DEFENITION
    defenition1 = re.findall('\[(\w{2,3}\.)?(.+?)(?:\((\w{2,3}\.)\))?\]', new_line)
    def_body = ''
    for defen in defenition1:
        def_body += '<def>\n<text>\n'+defen[1]+'<text>\n<lang lang_code="" source="">\n'+defen[0]+'</lang>\n</def>\n'
    new_line = re.sub('\[(\w{2,3}\.)?.+?(?:\(\w{2,3}\.\))?\]', '', new_line)

    defenition2 = re.findall('\[(.+?)\((.+?)\)\]', new_line)
    for defen in defenition2:
        def_body += '<def>\n<text>\n'+defen[0]+'</text>\n<source n="1" source_code="">\n'+defen[1]+'</source>\n</def>\n'
    new_line = re.sub('\[.+?\(.+?\)\]', '', new_line)

    # w.write('D' + def_body + '\n')
    print ('DEF', def_body)


    ### COMPARISON
    comparison = re.findall('[Сс]р\. ?<(.+?)>', new_line)
    comp_body = ''
    for c in comparison:
        comps = re.split(' и |, ?', c)
        comp_body = '<xr type="syn">\n<lbl>Сравни с</lbl>\n'
        i = 1
        for comp in comps:
            comp_body += '<ref n="'+str(i)+'">\n'+comp+'</ref>\n'
            i += 1
        comp_body += '</xr>\n'

        # w.write('C ' + comp_body + '\n')
        print('COMP', comps)

    new_line = re.sub('[Сс]р\. ?<.+?>', '', new_line)


    ### ANTONYM
    antonym = re.findall('[Пп]рот\. ?<(.+?)>', new_line)
    ant_body = ''
    for a in antonym:
        ants = re.split(' и |, ?', a)
        ant_body = '<xr type="ant">\n<lbl>\nПротивопоставление с</lbl>\n'
        i = 1
        for ant in ants:
            ant_body += '<ref n="' + str(i) + '">\n' + ant + '</ref>\n'
            i += 1
        ant_body += '</xr>\n'

        # w.write('A' + ant_body + '\n')
        print('ANT', antonym)

    new_line = re.sub('[Пп]рот\. ?<.+?>', '', new_line)


    ### IDIOM
    idioms = re.findall('\|+ ?([-\w\(\) ,.?!;]+?) ?(?:\n|[Сс]м\.)', new_line)
    id_body = ''
    for idiom in idioms:
        ids = re.split(', ?', idiom)
        id_body = ''
        i = 1
        for id in ids:
            id_body += '<re type="idiom">\n<quote>\n'+id+'</quote>\n</re>\n'
            i += 1

        # w.write('I' + id_body + '\n')
        print('ID', ids)

    new_line = re.sub('\|+ ?[-\w\(\) ,.?!;]+? ?(?:\n|[Сс]м\.)', '', new_line)


    ### EXAMPLE
    examples = []
    examples1 = re.findall('// ?([^\">]+?)\. ?(.+?)\.', new_line)
    new_line = re.sub('// ?[^\">]+?\. ?.+?\.', '', new_line)
    examples2 = re.findall('[\"<](.+?)[\">]\.? ?(.+?)\.', new_line)
    new_line = re.sub('[\"<](.+?)[\">]\.? ?(.+?)\.', '', new_line)
    examples3 = re.findall('\. ?([А-Я].+?)[\">]\.? ?(.+?)\.', new_line)
    new_line = re.sub('\. ?([А-Я].+?)[\">]\.? ?(.+?)\.', '', new_line)
    examples += examples1 + examples2 + examples3
    ex_body = ''
    for ex in examples:
        ex_body += '<cit type="example">\n<quote>\n'+ex[0]+'</quote>\n<author>\n'+ex[1]+'</author>\n</cit>\n'
    examples4 = re.findall('<(.+?)>\.', new_line)
    new_line = re.sub('<(.+?)>\.', '', new_line)
    if examples4:
        ex_body += '<cit type="example">\n<quote>\n'+examples4[0]+'</quote>\n</cit>\n'

    # w.write('EX' + ex_body + '\n')
    print ('EX', examples)


    ### FORM
    forms = re.findall('^[-\w .!]+\(([-\w .,]+?)\)', new_line)
    sex_body = ''
    form_body = ''
    for f in forms:
        sex_body += '<sex_parall>\n'+ ', '.join(forms)+'</sex_parall>\n'
        form_body += '<form type="inflected">\n<orth>\n'+ ', '.join(forms)+'</orth>\n</form>\n'

        # w.write('F ' + sex_body + '\n')
        print('FOR', ', '.join(forms))

    new_line = re.sub('\([-\w .,]+?\)', '', new_line)


    ### SYNONYM
    syn_contexts = re.findall('([-\w\(\) .!]*?)[;,:] ?(.+?)$', new_line)
    cont_body = ''
    syns = []
    for context in syn_contexts:
        contexts = re.split('[;.]', syn_contexts[0][1])
        for cont in contexts:
            cont = re.sub('(^ +| +$)', '', cont)
            if ',' in cont:
                cont_body += '<xr type="syn">\n<group>\n'+cont+'</group>\n</xr>\n'
            elif ' ' in cont:
                syns.append(cont)

    syn_body = ''
    i = 1
    for syn in syns:
        syn_body += '<ref n="'+str(i)+'">\n'+syn+'</ref>\n'
        i += 1
    if syn_body != '':
        syn_body = '<xr type="syn">\n'+syn_body+'</xr>\n'

    # w.write('CON' + cont_body + '\n')
    print('CON', syns)

    new_line = re.sub('[;,:] ?(.+?)$', '', new_line)


    ### WORD
    input = re.findall('[-\w !.]+', new_line)
    word_body = ''
    if input != []:
        word = re.sub(' +$', '', input[0])
        word_body += '<entry type="main">\n<form>\n<orth main="True">\n'+word+'</orth>\n</form>\n'
    new_line = re.sub('[-\w !.]+', '', new_line)

    # w.write('W ' + word_body + '\n')
    print ('W', word)

    # w.write('=' * 30 + '\n')
    print ('='*30)

    body += word_body + \
              form_body + \
              '<sense n="1">\n' + \
              def_body + \
              ex_body + \
              sex_body + \
              comp_body + \
              ref_body + \
              cont_body + \
              syn_body + \
              ant_body + \
              '</sense>\n' + \
              id_body + \
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
         '<title volume="1" dict_id="">Словарь русских синонимов и сходных по смыслу выражений</title>\n' \
         '<author>Наум Абрамович Переферкович</author>\n' \
         '<pubdate>1900</pubdate>\n' \
         '</head>\n' \
         '<dict_lang>\n' \
         '<language n="content">\n' \
         '<idno type="iso639-3">rus</idno>\n' \
         '</language>\n' \
         '</dict_lang>\n' \
         '</front>\n' \
         '<body>\n' \
         '<div>\n' \
         '<superEntry>\n'

footer = '</superEntry>\n' \
         '</div>\n' \
         '</body>\n' \
         '<xml>\n'

main = header + body + footer
w.write(main)

