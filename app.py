from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Compromisso
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


compromisso_tag = Tag(
    name="Compromisso", description="Adição, visualização, edição e remoção de compromissos à base")


@app.get('/', tags=[compromisso_tag])
def home():
    """Redireciona para a documentação Swagger.
    """
    return redirect('/openapi/swagger')


@app.post('/adiciona-compromisso', tags=[compromisso_tag],
          responses={"200": CompromissoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_compromisso(form: CompromissoCreateSchema):
    """Adiciona um novo Compromisso à base de dados

    Retorna uma representação dos compromissos associados.
    """
    compromisso = Compromisso(
        nome=form.nome)
    try:
        session = Session()
        session.add(compromisso)
        session.commit()
        return apresenta_compromisso(compromisso), 200

    except IntegrityError as e:
        error_msg = "Compromisso de mesmo nome já salvo na base."
        return {"mensagem": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo item."
        return {"mensagem": error_msg}, 400


@app.put('/atualiza-compromisso', tags=[compromisso_tag],
         responses={"200": CompromissoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_compromisso(form: CompromissoUpdateSchema):
    """Edita um compromisso na base de dados"""
    try:
        session = Session()
        compromisso = session.query(Compromisso).filter(
            Compromisso.id == form.id).first()

        if compromisso is None:
            raise HTTPException(
                status_code=404, detail="Compromisso não encontrado")

        compromisso.nome = form.nome
        session.commit()

        return apresenta_compromisso(compromisso), 200

    except IntegrityError as e:
        error_msg = "Compromisso de mesmo nome já salvo na base."
        return {"mensagem": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível atualizar o compromisso."
        return {"mensagem": error_msg}, 400


@app.get('/lista-compromissos', tags=[compromisso_tag],
         responses={"200": ListagemCompromissoSchema, "404": ErrorSchema})
def get_compromissos():
    """Faz a busca por todos os Compromissos cadastrados

    Retorna uma representação da listagem de compromissos.
    """
    session = Session()
    compromissos = session.query(Compromisso).all()

    if not compromissos:
        return {"compromissos": []}, 200
    else:
        print(compromissos)
        return apresenta_compromissos(compromissos), 200


@app.get('/lista-um-compromisso', tags=[compromisso_tag],
         responses={"200": CompromissoViewSchema, "404": ErrorSchema})
def get_compromisso(query: CompromissoBuscaSchema):
    """Faz a busca por um Compromisso a partir do NOME do compromisso

    Retorna uma representação dos compromissos.
    """
    compromisso_nome = query.nome
    session = Session()
    compromisso = session.query(Compromisso).filter(
        Compromisso.nome == compromisso_nome).first()

    if not compromisso:
        error_msg = "Compromisso não encontrado na base."
        return {"mensagem": error_msg}, 404
    else:
        return apresenta_compromisso(compromisso), 200


@app.delete('/deleta-compromisso', tags=[compromisso_tag],
            responses={"200": CompromissoDelSchema, "404": ErrorSchema})
def del_compromisso(query: CompromissoBuscaSchema):
    """Deleta um Compromisso a partir do nome de compromisso informado

    Retorna uma mensagem de confirmação da remoção.
    """
    compromisso_nome = unquote(unquote(query.nome))
    print(compromisso_nome)
    session = Session()
    count = session.query(Compromisso).filter(
        Compromisso.nome == compromisso_nome).delete()
    session.commit()

    if count:
        return {"mensagem": "Compromisso removido", "nome": compromisso_nome}
    else:
        error_msg = "Compromisso não encontrado na base."
        return {"mensagem": error_msg}, 404
