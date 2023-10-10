import { 
    Icon,
    Button, 
    Input } from '@chakra-ui/react'
  

import { FiUpload } from 'react-icons/fi';
import axios from 'axios'
import { useRef, useState } from 'react';


  
  function UploadButton() {
    
    //variable que guarda el file
    const [selectedFile, setSelectedFile] = useState(null);

    //refencia al componente Input
    const fileInputRef = useRef(null);


    //esta funcion envia un file.txt al API y  devolver una matriz 
    const sendMap = async () =>  {
      try {
        console.log(selectedFile)
        const data = {'file': selectedFile}
        console.log(data)
        const response = await axios.post('http://127.0.0.1:5000/load_file', data);

        if (response.status === 200) {
          const message = response.data.message
          localStorage.setItem("matrizMap",message)
          console.log('mensaje del API:', message)
          const responseLocal=localStorage.getItem("matrizMap")
          console.log("respuesta del get LocalStorage", responseLocal)
        } else {
          console.error('La llamada al API fallo')
        }
  
      } catch (error) {
        console.error('Error al enviar el archivo', error)
      }
    }
  
    //manejo el input para que guarde el archivo y lo envie
    function handleFileSelected(e) {
      const file = e.target.files[0];
      if(file) {
        console.log('file',file)
        console.log(file.name)
        console.log('contenido', file.size)

        if (file.type === 'text/plain') {
          const reader = new FileReader();
          reader.onload = (e) => {
            const fileContent = e.target.result;
            console.log('Contenido del archivo:', fileContent);
          };
          reader.readAsText(file);
        }
    


        setSelectedFile(file);
        console.log('seletex',selectedFile)
        //sendMap(); 
      }
    }
  
    //Cuando el boton es presiona da click al input
    function handleFileButton() {
      fileInputRef.current.click();
    }
  
    return ( 
      <>
          <Input 
            display='none'
            type='file'
            accept='.txt'
            ref={fileInputRef}
            onChange={handleFileSelected} />
  
          <Button 
            type='file' 
            rightIcon={<Icon as={FiUpload}/>} 
            colorScheme='blue'
            onClick={handleFileButton}>
                Upload
          </Button>
          
     
      </>
    )
  }
  
  export default UploadButton;
  