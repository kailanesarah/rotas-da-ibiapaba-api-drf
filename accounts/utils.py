
#
'''

Esse método consegue lidar com campos relacionados, como Many-to-Many e Reverse Foreign Keys
O Django Admin não permite que esses tipos de campos sejam usados diretamente no list_display. 
Então, a solução é criar uma classe para fazer a extração desses campos e dos seus dados.

Aqui nesse caso, o metodo pode pegar qualquer campo que possua uma relação Foreign Key ou Many to Many
Ele faz isso: Primeiro pega o objeto passado para o django (enviado via json) ou já cadastrado no
campo e pega apenas o que querenos, nesse caso o name_field e guarda, logo em seguida ele garante
que esse obj ele possui uma relação many to many. Se sim, ele percorre esse obj, transforma em string
e logo em seguida junta todos os itens em uma lista... estudar mais sobre o assunto neunn'''


class RelatedFieldExtractorAdmin():
    def get_field(self, obj, name_field):
            related_manager = getattr(obj, name_field)
            if hasattr(related_manager, 'all'):
                  return ", ".join([str(item) for item in related_manager.all()])
        