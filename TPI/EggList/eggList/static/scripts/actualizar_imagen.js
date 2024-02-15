inputs_imagen = document.getElementsByClassName("input-imagen");
        imagenes = document.getElementsByClassName("imagen");

        
        inputs_imagen[0].addEventListener("change", (event)=>{
            const file = event.target.files[0]
            if (file){
                const reader = new FileReader()
                reader.addEventListener("load",(readerEvent) =>{
                    imagenes[0].setAttribute('src', readerEvent.target.result)
                })
                reader.readAsDataURL(file)
            };
                
            }      
            )