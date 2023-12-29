import flet as ft
import aiohttp
import asyncio

pokemon_actual = 0

async def main(page: ft.Page):
    
    page.window_width = 480
    page.window_height = 720
    page.window_resizable = False
    page.padding = 0
    page.fonts ={
        "zpix" : "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf",}

    page.theme = ft.Theme(font_family="zpix")
    

    async def peticion(url):
        async with aiohttp.ClientSession() as session:
            #async with session.get(url) as response: #Linea de codigo correcta,
            #instalar certificados SSL para tener uan conexión segura
            async with session.get(url, ssl=False) as response: #Linea de codigo "temporal"
                return await response.json()
########################################################

    async def info_pokemon(e:ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flechasup:
            pokemon_actual += 1
        
        else:
            pokemon_actual -= 1

        num = (pokemon_actual%301)

        try:
            result = await peticion (f"https://pokeapi.co/api/v2/pokemon/{num}")
            print (result["name"])#["abilities"][0]["ability"]["name"])

            datos = f"Name:{result["name"]}\n\aAbilities:"
            for elemento in result["abilities"]:
                habilidad = elemento["ability"]["name"]
                datos += f"\n{habilidad}"
            datos += f"\n\nHeight: {result["height"]}"
            texto.value = datos
            imagen.src = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{num}.png"
            await page.update_async()
        except Exception as e:
            print(f"Error al cargar la imagen:{e}")
        
    async def luces():
            while True:
                await asyncio.sleep(1)
                lucecita.bgcolor =ft.colors.BLUE
                await page.update_async()
                await asyncio.sleep(0.1)
                lucecita.bgcolor = ft.colors.BLUE_900
                await page.update_async()


#########################################################
    lucecita = ft.Container(width=59, height=58,left=5.6,top=5,bgcolor=ft.colors.BLUE_500, border_radius=40)

    button_blue = ft.Stack([
        ft.Container(width=70, height=69,bgcolor=ft.colors.BLACK87, border_radius=42),
        lucecita
    ])
    elementos_superior = [
        ft.Container(button_blue,width=70, height=70),
        ft.Container(width=30, height=30,bgcolor=ft.colors.RED_ACCENT,border_radius=30),
        ft.Container(width=30, height=30,bgcolor=ft.colors.GREEN_600,border_radius=30),
        ft.Container(width=30, height=30,bgcolor=ft.colors.YELLOW_600,border_radius=30),

    ]

    poke_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"

    imagen = ft.Image(
        src = poke_url,
        scale = 5,
        width=30,
        height=30, 
        top=200/2,
        left= 190)

    stack_central = ft.Stack([
        ft.Container(width=450,height=300,bgcolor=ft.colors.WHITE,border_radius=20),
        ft.Container(width=350,height=200,bgcolor=ft.colors.BLACK, top=20,left=25),
        imagen,
        
    ])

    """
    triangulos = ft.canvas.Canvas([
        ft.canvas.Path([
            
            ft.canvas.Path.MoveTo(38,0),
            ft.canvas.Path.LineTo(0,28),
            ft.canvas.Path.LineTo(28,28),
            
        ],
        paint = ft.Paint(
            style = ft.PaintingStyle.FILL,

            )
        )
    ])
    """

    lado = 40  # longitud del lado del triángulo
    altura = lado * (3**0.5) / 2  # altura de un triángulo equilátero

    # Definir el camino del triángulo equilátero
    pulsador = ft.canvas.Canvas([
    ft.canvas.Path([
        ft.canvas.Path.MoveTo(0, 0),
        ft.canvas.Path.LineTo(lado, 0),
        ft.canvas.Path.LineTo(lado / 2, altura),
        ft.canvas.Path.LineTo(0, 0),
    ]),
    ])


    flechadown = ft.Container(pulsador,width=40,height=40,on_click=info_pokemon)

    flechasup = ft.Container(pulsador,rotate=ft.Rotate(angle=3.14159),width=40,height=40,on_click=info_pokemon)

    flechas = ft.Column(
        [
        #radianes 180 grados = 3.14159 
        ft.Container(pulsador,rotate=ft.Rotate(angle=3.14159),width=40,height=40,on_click=info_pokemon),
        ft.Container(pulsador,width=40,height=40,on_click=info_pokemon)

        ]
    )

    texto = ft.Text(
        value="...",
        color= ft.colors.WHITE38,
        size=15,
    )

    elementos_inferiores =[
        ft.Container(width=50, ),#MARGEN IZQUIERDO
        ft.Container(texto,padding=18,width=250,height=200,bgcolor=ft.colors.PURPLE, border_radius=20),
        ft.Container(width=30, ),#MARGEN DERECHO
        ft.Container(flechas,width=40,height=80),
        
        
    ] 

    superior = ft.Container(content=ft.Row(elementos_superior),width=400, height=70, margin = ft.margin.only(top=20))
    centro = ft.Container(content=stack_central,width=400, height=240, margin=ft.margin.only(top=20)
                        ,alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(elementos_inferiores),width=400, height=240, margin = ft.margin.only(top=20),)

    col = ft.Column(spacing=0,controls=[
        superior,
        centro, 
        inferior,
    ])

    contenedor = ft.Container(col, width=480, height=720,bgcolor=ft.colors.RED,alignment=ft.alignment.top_center)

    await page.add_async(contenedor)
    await luces()
    

ft.app(target=main)

#Falta arreglar uno de los pulsadores
#otra prueba con git