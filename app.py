from flask import Flask, render_template
from handler import ner_handler, search_entity_handler, search_relation_handler
from forms import NerForm, EntityForm, RelationForm


app = Flask(__name__)
app.secret_key = 'secret key'
app.config['WTF_I18N_ENABLED'] = False


@app.route('/')
def index():
    ner_form = NerForm()
    return render_template('index.html', form=ner_form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/search_entity', methods=['GET', 'POST'])
def search_entity():
    entity_form = EntityForm()
    res = {'ctx': 'padding', 'entityRelation': ''}
    if entity_form.validate_on_submit():
        res = search_entity_handler.search_entity(entity_form.entity.data)
    return render_template('entity.html', form=entity_form, ctx=res['ctx'], entityRelation=res['entityRelation'])

@app.route('/search_relation', methods=['GET', 'POST'])
def search_relation():
    relation_form = RelationForm()
    res = {'ctx': '', 'searchResult': ''}
    if relation_form.validate_on_submit():
        res = search_relation_handler.search_relation(relation_form.entity1.data, relation_form.relation.data, relation_form.entity2.data)
    return render_template('relation.html', form=relation_form, ctx=res['ctx'], searchResult=res['searchResult'])

@app.route('/ner-post', methods=['POST'])
def ner_post():
    ner_form = NerForm()
    ctx = {'rlt': '', 'seg_word': ''}
    if ner_form.validate_on_submit():
        ctx = ner_handler.ner_post(ner_form.ner_text.data)
    return render_template("index.html", form=ner_form, rlt=ctx['rlt'], seg_word=ctx['seg_word'])
