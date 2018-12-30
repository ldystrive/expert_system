from src.expert import ExpertSystem
import eel

eel.init('web')
es = ExpertSystem()
es.readRule('src/rule.txt')

@eel.expose
def receiveData(headShape, headSize, bodySize, fat, legs, \
    hairLength, tailLength, eyesShape, earsSize, earsShape, temperament):
    
    conditions = []
    conditions.append('head_shape is ' + headShape)
    conditions.append('head_size is ' + headSize)
    conditions.append('body_size is ' + bodySize)
    conditions.append('fat is true' if fat else 'fat is false')
    conditions.append('legs is ' + legs)
    conditions.append('hair_length is ' + hairLength)
    conditions.append('tail_length is ' + tailLength)
    conditions.append('eyes_shape is ' + eyesShape)
    conditions.append('ears_size is ' + earsSize)
    conditions.append('ears_shape is ' + earsShape)
    conditions.append('temperament is ' + temperament)
    cat = es.engineWork(conditions)
    if cat is None:
        cat = 'default'
    eel.receiveImg(cat)


eel.start('index.html', size=(1000, 770))