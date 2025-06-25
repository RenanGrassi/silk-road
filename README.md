# silk-road
Repositório para nosso sistema distribuído da disciplina.

## Erros comuns, e como resolver
```sh
silk-road-client  | This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
silk-road-client  | 
silk-road-client  | Available platform plugins are: offscreen, minimalegl, wayland-egl, wayland, linuxfb, vkkhrdisplay, minimal, eglfs, xcb, vnc.
```
Para resolver esse, precisa apenas de conceder permissão ao docker, com:
```sh
xhost +local:docker
```

## Documentação
### Sockets de comunicação
#### Servidor
Para realizar a troca de mensagens, foi criado um socket, implantado por uma classe, e startado em uma thread de processo, utilizando o asyncio para rodar de maneira concorrente, com o método
```py
async def start(self):
    self.server = await asyncio.start_server(
        self.handle_client, self.host, self.port
    )
    addr = self.server.sockets[0].getsockname()
    print(f"Escutando em {addr}")
    async with self.server:
        await self.server.serve_forever()
```

Quando um servidor detecta uma nova conexão de um cliente, invoca um método de classe, abrindo um canal de comunicação com o mesmo através da seguinte função que também está encapsulada na classe de socket
```py
async def handle_client(self, reader, writer):
    try:
        while True:
            data = await self.read_msg(reader)
            try:
                decoded = json.loads(data.decode())
                if type(decoded) is str:
                    print(f"Recebido: {decoded}, {type(decoded)}")
                    decoded = json.loads(decoded)
                print(f"Recebido: {decoded}, {type(decoded)}")
                if not decoded.get("group") and not decoded.get("route"):
                    await self.send_error("Grupo ou rota não encontrados", writer)
                    continue
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                await self.send_error("Erro ao decodificar JSON", writer)
                continue
            dto = BaseDTO(**decoded)
            try:
                response = self.router.find_route(dto)
                await self.send_success(
                    {"type": "SUCCESS", "data": response}, writer
                )
            except Exception as e:
                await self.send_error(e.__str__(), writer)
                continue
    except asyncio.IncompleteReadError as e:
        print(e)
    writer.close()
    await writer.wait_closed()
```
Essa função é responsável por estabelecer a conexão com o cliente, interpretar a mensagem, e enviar a resposta do servidor para o mesmo. Nos outros tópicos será abordado como essa mensagem é decodificada, o tipo esperado, dentre outros tópicos.

Além disso, também existe o método de encerrar o servidor, fechando as conexões ativas, e tirando o servidor do status de listener, isso se dá pela função stop, que também é um método dessa classe
```py
async def stop(self):
    if self.server:
        self.server.close()
        await self.server.wait_closed()
        print("Servidor encerrado.")
    else:
        print("Servidor não está em execução.")
```
### Parser de mensagens
#### Servidor
##### Leitura
Para fazer o parser das mensagens, utilizamos os 4 primeiros bits para encapsular o tamanho das mensagens, o que é essencial no decoder. Optamos pelo formato JSON no envio, para facilitar o decode e o tratamento dos objetos como **dicts** no python.
Para formatar a mensagem, nos utilizamos dessa função
```py
async def read_msg(self, reader):
    raw_len = await reader.readexactly(4)
    msg_len = struct.unpack(">I", raw_len)[0]  # big-endian uint32
    data = await reader.readexactly(msg_len)
    return data
```
Como estamos esperando um tipo de mensagem, é importante sermos resilientes, e tratar exceções de erros de parser na mensagem recebida, e olhando para a função **handle_client**, temos um tratamento, utilizando um try/except:
```py
try:
    decoded = json.loads(data.decode())
    if type(decoded) is str:
        print(f"Recebido: {decoded}, {type(decoded)}")
        decoded = json.loads(decoded)
    print(f"Recebido: {decoded}, {type(decoded)}")
    if not decoded.get("group") and not decoded.get("route"):
        await self.send_error("Grupo ou rota não encontrados", writer)
        continue
except json.JSONDecodeError as e:
    print(f"Erro ao decodificar JSON: {e}")
    await self.send_error("Erro ao decodificar JSON", writer)
    continue
```
Basicamente, neste trecho, estamos tentando ler a mensagem, e caso isso não seja possível por erro no json, enviamos para o cliente uma mensagem de erro.

##### Resposta
Essa questão da mensagem ser um json, e de ser passado o tamanho nos 4 primeiros bits, também deve ser o padrão de resposta do servidor, e para isso, existe a função send_message, que é responsável por fazer o encode desses dicts
```py
async def send_message(self, writer, msg_bytes):
    writer.write(struct.pack(">I", len(msg_bytes)))
    writer.write(msg_bytes)
    await writer.drain()
```
Outro fator importante no envio de mensagens do lado do servidor, é o fato da informação ter sido enviada com sucesso, ou se tiver tido algum tipo de erro ou exceção no meio do caminho. É de extrema importância que a aplicação seja resiliente, e para isso, trate exceções. Para esses casos, temos 2 tipos de resposta, sendo elas descritas como **ERROR**, ou **SUCCESS**. Para tal, utilizamos duas funções, que encapsulam o resultado esperado em um campo denominado TYPE, do nosso JSON, para que possa ser tratado do lado do cliente
```py
async def send_success(self, message: dict, writer):
    success_message = {"type": "SUCCESS", "data": message}
    return await self.send_message(writer, json.dumps(success_message).encode())

async def send_error(self, message: str, writer):
    error_message = {"type": "ERROR", "data": {"clasure": message}}
    return await self.send_message(writer, json.dumps(error_message).encode())
```
Para explicar sobre como esses erros são mapeados, precisamos voltar na nossa função de socket, onde lidamos com a requisição do cliente, mais especificamente neste trecho, na função **handle_client**
```py
try:
    response = self.router.find_route(dto)
    await self.send_success(
        {"type": "SUCCESS", "data": response}, writer
    )
except Exception as e:
    await self.send_error(e.__str__(), writer)
    continue
```
O tratamento de exceção acontece de maneira generalizada, enviando com sucesso caso não tenha sido gerado nenhuma, e caso esteja, mandando a exceção como string para o cliente.
### Mapeamento de funções do lado do servidor
O mapeamento do que vai ser executado, é dado através de dois parâmetros no json, denominados **group** e **route**, para fazer internamente o mapeamento, foi criado uma classe abstrata, que força a implementação de um atributo denominado group
```py
from abc import ABC, abstractmethod


class AbstractRoute(ABC):
    """
    Abstract base class for routes.
    """

    @classmethod
    def group(self) -> str:
        """
        The path of the route.
        :return: The path of the route.
        """
        raise NotImplementedError()

```
Essa clases, é a de entrada de chamados, e o "group", é exatamente o que deve ser passado pelo cliente, ou seja, o recurso que ele quer acessar.
Já o atributo **route**, se refere a um método da classe que contêm aquele grupo, ou seja, uma classe que implementa AbstractRoute, têm seu método de classe definido como, por exemplo, **users**, e têm um método denominado **get_all**. Para o cliente requerer a informação fornecida por esse objeto, pode mandar uma mensagem com esse formato
```json
{
    "group": "users",
    "route": "get_all",
    "conf": {}
}
```
Para obtermos a classe a ser invocada, utilizamos uma classe auxiliar, que é responsável por coletar todas as classes herdadas de AbstractRoute, e que têm seu arquivo denominado routes.py Com base nisso, essa classe no init, obtêm todas através do módulo importlib, lendo as correspondentes, e armazenando em uma lista
```py
from src.abstracts.base_request import BaseDTO
import os
from src.abstracts.abstract_route import AbstractRoute
import importlib
import inspect


class RouteRequests:
    """
    Class to find the route for a given request.
    """

    def __init__(self):
        """
        Initialize the RouteRequests class.
        """

        self.routes: list[AbstractRoute] = self.find_route_classes()
        print(f"Routes: {self.routes}")

    def find_route_classes(self, path: str | None = None):
        """
        Find recursively the route in modules/*/*/routes.py.
        """
        # Iterate through all routes
        base_dir = (
            os.path.join(os.path.dirname(__file__), "..", "modules")
            if path is None
            else path
        )
        classes = []
        for module_dir in os.listdir(base_dir):
            module_path = os.path.join(base_dir, module_dir)
            print(f"Module path: {module_path}")
            if module_path.endswith("routes.py") and os.path.isfile(module_path):
                # Dynamically import the routes.py file
                spec = importlib.util.spec_from_file_location("routes", module_path)
                routes_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(routes_module)
                inspect_classes = inspect.getmembers(routes_module, inspect.isclass)
                route_classes = [
                    cls
                    for name, cls in inspect_classes
                    if issubclass(cls, AbstractRoute) and cls is not AbstractRoute
                ]
                classes.extend(route_classes)
            elif os.path.isdir(module_path):
                classes.extend(self.find_route_classes(module_path))
        return classes
```
A classe inspect, após o módulo ser importado, itera sobre o arquivo, obtendo todas as classes, e depois filtrando por aquelas que herdam de AbstractRoute, garantindo que apenas classes específicas sejam importadas.

No módulo handle_client, chamamos um método dessa classe, que passa por todas as classes disponíveis buscando a solicitada pelo cliente, através dos parâmetros já discutidos aqui, e fazendo uma chamada de método
```py
def find_route(self, dto: BaseDTO):
    """
    Find the route for the given request.
    """
    # Get the request method and path
    groups = [cls.group() for cls in self.routes]
    print(f"Grupos: {groups}")
    class_group = next(
        (cls for cls in self.routes if cls.group() == dto.group), None
    )
    if class_group is None:
        print(f"Grupo {dto.group} não encontrado.")
        return None
    instance = class_group()
    method = getattr(instance, dto.method, None)
    if method is None:
        print(f"Método {dto.method} não encontrado.")
        return None
    # Call the method and return the result
    return method(dto.conf)
```
### Login e autenticação
```json
{
    "group": "users",
    "method": "login",
    "conf": {
        "email": "murillo@gmail.com",
        "password": "123456"
    }
}
```
```json
{
        "group": "users",
        "method": "get",
        "conf": {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im11cmlsbG9AZ21haWwuY29tIiwiaWQiOjEsImV4cCI6MTc0ODcxMTUxMn0.mcAECHhSIWUstdwz3VD2FGHHCoT6UEPGkd0dzR8_Rsc"
        }
}
```
```json
{
        "group": "users",
        "method": "create",
        "conf": {
            "email": "teste2@gmail.com",
            "password": "123456",
            "name": "MurilloMurillo2"
        }
}
```
### Produtos
```json
{
        "group": "products",
        "method": "list",
        "conf": {}
}
```
### Usuários