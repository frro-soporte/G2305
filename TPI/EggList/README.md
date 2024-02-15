
<h1>EggList</h1>


Integrantes:
Buschittari Nahuel  (nahubuschittari0310@gmail.com)
Coronel Nahuel Eghar (nahucarc2@gmail.com)
Marincioni Alejandro (alemarincionii@gmail.com)
Taborra Facundo (taborrafacundo@gmail.com)

				




<h2>Documentacion</h2>








<h4> Introducción </h4>
En la actualidad, es comun que las compras semanales se realicen mediante una aplicación. Sin embargo, muchas personas prefieren aún visitar físicamente la tienda. Durante este proceso puede presentar desafíos, como olvidar lo que se necesitaba comprar o perder la lista de papel donde se anotaron los productos. Incluso con métodos más avanzados, como el uso de mensajes de WhatsApp para armar la lista, persisten problemas de organización significativos. Para abordar estas dificultades, el Grupo 5 ha desarrollado una solución innovadora.

<h4> Descripción del proyecto </h4>

EggList es una aplicación diseñada para crear listas de compras virtuales y colaborativas. Durante la semana, los usuarios ir gregando los productos que necesitan a una lista, la cual estará disponible cuando sea el momento de hacer la compra. Esta aplicación permite la colaboración entre múltiples usuarios, manteniendo un registro claro de quién creó la lista y quién añadió cada producto a la misma. Para facilitar esta colaboración, los usuarios se organizan en lo que se denomina "Grupo Familiar".
Además, al momento de realizar la compra, EggList permite ingresar los precios y cantidades de los productos, mostrando el total en tiempo real. Esto brinda la posibilidad de comparar los costos previstos con los gastos reales mientras se está en la tienda.
Una vez completada la compra, la aplicación registra la transacción y ofrece acceso a un historial detallado de compras para cada usuario. Esto facilita el seguimiento del gasto y la planificación de futuras compras.


<h4> Aplicación </h4>
Esta es la aplicación lista para usar
https://egglist.up.railway.app/
<h4> Stack tecnológico
Python 
Flask
JInja2
SqlAlchemy
HTML
CSS
JS
BoxIcon

<h4> Librerías utilizadas </h4>
Flask
SQLAlchemy
Flask-WTF -> Para manejar formularios y validaciones de los mismos
Flask-Mail -> Para poder enviar correos
Flask-Login -> Permite manejar los login de los usuarios de manera mas simple
Flask-Migrate -> Para realizar migraciones de la BBDD
Bcrypt -> Manejo de encriptaciones de contraseñas 
itsdangerous -> Permite gestionar los tokens (usado a la hora de invitar usuarios a grupo familiar o del registro de los mismos)
Folium -> Crear mapas que pueda visualizar el usuario
PIL -> Manejo de imágenes


<h4> Modelo del sistema </h4>
<img src="https://i.ibb.co/VSQTKd5/modelo-egglist.png" alt="modelo-egglist" border="0" />

<h4> Requiermientos Funcionales </h4>
<h6> Para un usuario </h6>
El sistema debe permitir que un usuario se registre y pueda loguearse.
Ademas, puede, una vez registrado, modificar su foto de perfil y cambiar los datos ingreados al momento del registro, como nombre, apellido, numero de telefono, email, etc.
Al momento de consultar el perfil de otras personas, el sistema permite el acceso a otros medios de comunicacion como whatsapp, correo o telefono de manera rapida.
Cabe recalcar que para poder utilizar la aplicacion, la persona debe ingresar la ciudad en la que se encuentra

<h6> Para un grupo familiar </h6>
La aplicación permite la creación de grupos familiares, la persona que cree el grupo sera el administrador del mismo.
El administrador del grupo familiar puede editar el nombre y imagen del grupo, e   invitar nuevos usuarios.
Ademas, tiene la posibilidad de eliminar a un usuario de un grupo

<h6> Para las Listas </h6>
El usuario puede crear listas de compra a su gusto.
En caso de poseerlo, tambien puede inlcuir al resto de integrantes de su grupo familiar a que participen de la lista.
Una lista para un usuario puede tener 2 posibles “vistas”:
Vista armador -> Presenta una version mas simplificada de la lista ideal para quienes arman la lista
Vista comprador -> Presenta ciertas funcionalidades agregadas, como agregar productos a un carrito virtual, ingresar el precio del producto, etc.
Para una lista,  se pueden agregar productos, modificarlos o borrarlos.
Para cada producto agregado figura que usuario lo agrego.


Para pasar de ser Armador a comprador, se tiene que seleccionar el supermercado en el cual se esta realizando la compra
Para las compras
Al momento que un Comprador finalizo su compra, esta misma se registra.
Esta puede ser accedida para consulta mas adelante, y se mostrará el total 


<h6> Aclaracion </h6>
Si vien en el modelo se ven algunas clases que estan de mas, la idea mas adelante es agregar el rol admin que permita administrar las ciudades y los supermercados, entre otras cosas, por eso es que se ven esas entidades en el sistema
Sin embargo, como son clases que solo sirven para consulta, no vimos urgente realizarlo ahora ya que lo manejamos todo desde la BBDD


<h4> Requerimientos No funcionales </h4>
El sistema debe asegurar que los datos están protegidos de acceso no autorizado
El sistema debe proporcionar mensajes de error informativos
El sistema debe dar confirmación cada vez que se realicen acciones sobre BBDD
La aplicación debe tener un diseño Responsive que permite funcionar bien tanto en celulares como en computadoras 
Se sigue el patrón MVC
Todas las confirmaciones e invitaciones se envían mediante correo electrónico
El sistema se divide en capas, estas capas son
Templates -> Donde se guardan todas la estructuras de la Interfaces de Usuario escritas en HTML
Controller -> Se especifican las rutas de acceso al sistema, se mapean los datos ingresados al modelo de objetos y se capturan las excepciones enviadas por la capa Logic para mostrar los errores correspondientes
Logic -> Se  realizan las validaciones de negocio del sistema, se comunica con la capa datos para realizar las consultas, etc
Datos -> La única capa que tiene acceso a la base de datos


<h4> Reglas de negocio </h4>
<h6> Validaciones </h6>
RN01: Un mail de Usuario que esté registrado y confirmado no se puede volver a utilizar
RN02: El nombre del grupo familiar no se puede repetir
RN03: Un mismo usuario puede estar en un solo Grupo Familiar a la vez
RN04: Las provincias, ciudades y supermercados sólo pueden ser cargados por aquellos usuarios con rol de Administrador
RN05: Solo el administrador del grupo familiar puede editar el mismo e invitar gente
RN06: Solo un usuario puede realizar la compra para una misma lista
RN07: Una compra sólo puede ser accedida por la persona que la compro
RN08: El usuario debe tener registrado un código postal para acceder al sistema

<h6> Calculo </h6>
RN09: El total gastado de un Producto es igual a la cantidad adquirida del mismo multiplicado por su precio unitario
RN10: El total gastado de una compra es la sumatoria de todos lo gastado en los productos(precio * cantidad) de esa compra
RN11: Los productos de una lista que faltan comprar son todos los productos de una lista que no estan en carrito al momento de realizar la compra

