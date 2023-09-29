# Hashzap
# Botão de iniciar chat
# Popup para entrar no chat
# Quando entrar no chat: (aparece para todo mundo)
#       a mensagem que você entrou no chat
#       o campo e o botão de enviar mensagem
# A cada mensagem que você envia (aparece para todo mundo)
#       Nome: Texto da mensagem

import flet as ft # para instalar: pip install flet

def main(pagina):
    texto = ft.Text('Hashzap', size= 25,color= ft.colors.PINK_900, weight=ft.FontWeight.W_900)

    chat = ft.Column()

    nome_usuario = ft.TextField(label='Digite seu nome...')

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem['tipo']

        if tipo == 'mensagem':
            texto_mensagem = mensagem['texto']
            usuario_mensagem = mensagem['usuario']
            # Adicionar a mensagem no chat
            chat.controls.append(ft.Text(f'{usuario_mensagem}: {texto_mensagem}'))
        else:
            usuario_mensagem = mensagem['usuario']
            # Aparece o usuário que entrou no chat sem ter digitado a mensagem
            chat.controls.append(ft.Text(f'{usuario_mensagem} entrou no chat!',
                                         size= 12,
                                         italic= True,
                                         color= ft.colors.BLUE_300,
                                         weight= ft.FontWeight.W_700))
        
        pagina.update()

    # PUBSUB (PUBLISH SUBSCRIBE)
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(e):
        # Enviar uma mensagem
        pagina.pubsub.send_all({'texto': campo_mensagem.value,
                                'usuario': nome_usuario.value,
                                'tipo': 'mensagem'})
        # Limpar o campo de mensagem
        campo_mensagem.value = ''
        pagina.update()

    campo_mensagem = ft.TextField(label='Digite sua mensagem...', on_submit= enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton('Enviar', on_click= enviar_mensagem)

    def entrar_popup(e):
        pagina.pubsub.send_all({'usuario': nome_usuario.value,
                                'tipo': 'entrada'})
        # Adicionar o chat
        pagina.add(chat)
        # Fechar o popup
        popup.open = False
        # Remover o botão "Iniciar chat"
        pagina.remove(botao_iniciar)
        #Remover o texto "Hashzap"
        pagina.remove(texto)
        # Criar o campo de mensagem do usuário
        # Criar o botão de enviar mensagem do usuário
        pagina.add(ft.Row([
            campo_mensagem,
            botao_enviar_mensagem
             ]))
        pagina.update()

    popup = ft.AlertDialog(
        open= False,
        modal= True,
        title= ft.Text('Bem vindo ao Hashzap'),
        content= nome_usuario,
        actions= [ft.ElevatedButton('Entrar', on_click=entrar_popup)]
    )

    def entrar_chat(e):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton('Iniciar chat', on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER, port=777)
