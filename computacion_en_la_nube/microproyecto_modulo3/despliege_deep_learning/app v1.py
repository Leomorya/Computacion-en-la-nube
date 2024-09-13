from gluoncv.model_zoo import get_model
import matplotlib.pyplot as plt
from mxnet import gluon, nd, image
from mxnet.gluon.data.vision import transforms
from gluoncv import utils
from PIL import Image
import io
import flask 
import gluoncv

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return flask.render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Clasificador de Imágenes</title>
        </head>
        <body>
            <h1>Clasificador de Imágenes CIFAR-10</h1>
            <form action="/predict" method="post" enctype="multipart/form-data">
                <input type="file" name="img" accept="image/*" required>
                <input type="submit" value="Clasificar imagen">
            </form>
        </body>
        </html>
    ''')

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if flask.request.method == "POST":
        if flask.request.files.get("img"):
            img = Image.open(io.BytesIO(flask.request.files["img"].read()))
            
            transform_fn = transforms.Compose([
            transforms.Resize(32),
            transforms.CenterCrop(32),
            transforms.ToTensor(),
            transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])])
            img = transform_fn(nd.array(img))
            
            model_name = 'ResNet50_v1d'
# download and load the pre-trained model
            net = gluoncv.model_zoo.get_model(model_name, pretrained=True)
            
            net = get_model('cifar_resnet20_v1', classes=10)
            net.load_parameters('net.params')
            pred = net(img.expand_dims(axis=0))
            #print(pred.shape)
            ind = nd.argmax(pred, axis=1).astype('int')
            #print(ind)


            class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                       'dog', 'frog', 'horse', 'ship', 'truck']
            
            prediction = 'La imagen de entrada es clasificada como" [%s], con probabilidad %.3f.' % (class_names[ind.asscalar()], nd.softmax(pred)[0][ind].asscalar())
            return flask.render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Resultado de la Clasificación</title>
                </head>
                <body>
                    <h1>Resultado</h1>
                    <p>{{ prediction }}</p>
                </body>
                </html>
            ''', prediction=prediction)
    else: 
        return "Por favor, usa el formulario para subir una imagen."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 
