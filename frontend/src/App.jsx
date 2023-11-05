import { 
  Box,
  Text,
  Icon, 
  Center, 
  Button,  
  VStack, 
  Heading,
  Input
} from '@chakra-ui/react'



import { FiUpload } from 'react-icons/fi';
import {FaPlay}  from "react-icons/fa6";

import BoxGrid from './components/BoxGrid';
import UploadButton from './components/UploadButton';

import { useRef, useEffect, useState } from 'react';
import axios from 'axios'

function App() {

  const fileInputRef = useRef(null);

  const  matrix =[ [0,0,2],
                   [0,1,0],
                   [3,0,0]];
 

  const [selectedFile, setSelectedFile] = useState([]);
  const [map, setMap] = useState(matrix);
  const [clickRun, setClickRun] = useState(false);
  const [miValor, setMiValor] = useState('');
  
 
  function handleClickRun() {
    setClickRun(true);
    
  }

  useEffect(()  => {
    if(clickRun) {
      console.log("entre al run")
      let x = 0
      const intervalId = setInterval(() => {
        if (x >= selectedFile.length) {
          setClickRun(false)
          clearInterval(intervalId); // Stop the interval when x exceeds the array length
          return;
        }
        setMap(selectedFile[x].matrix)
        x=x+1
      }, 500);

      return () => clearInterval(intervalId);
    }
    
  }, [clickRun]);


  //Cuando el boton es presionado  click al input
  function handleFileButton() {
    fileInputRef.current.click();
  }

  //maneja el input para que guarde el archivo y lo envie
  function handleFileSelected(e) {

    
    const file = e.target.files[0];

    console.log(file)
    const reader = new FileReader();

    reader.onload = function(event) {
        const content = event.target.result;
        const lines = content.trim().split(/\n/).map(row => row.split(/\s/))
        const matriz = lines.map(row => row.map(bit => parseInt(bit)));

        setMap(matriz)
        console.log(matriz);
    };

    reader.readAsText(file);


    
    if(file) {
      
      const formData = new FormData
      formData.append("file", file)

      fetch('http://localhost:8000/uploadfile', {
        method: 'POST',
        body: formData,
      })

     .then(response => response.json())  

     .then(data => {
         
         //setMap(data.arrays[1].matrix);
        //console.log(data.arrays[0].matrix)
         setSelectedFile(data.arrays)

      })

      .catch(error => {
         console.error('Error al subir el archivo:', error);
       
      });
     


    }
    
  }

  


  return (
      <Center h='100%'>
      <VStack gap={5}>  

        <Heading  color='black'>Algoritmos de Busqueda</Heading>


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
        
      
        <BoxGrid matriz={map} />

        <Button  
          rightIcon={<Icon as = {FaPlay} />}
          colorScheme='whatsapp'
          onClick={handleClickRun}>
            Start
        </Button>

        <Box><Text color={'black'}>{miValor}</Text></Box>

      </VStack>
      </Center>
  )
}

export default App
