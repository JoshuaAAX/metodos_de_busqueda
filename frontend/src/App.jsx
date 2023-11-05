import { 
  Box,
  Text,
  Icon, 
  Center, 
  Button,  
  VStack, 
  Heading,
  Input,
  HStack,
  Select,
  Menu,
  MenuButton,
  MenuList,
  MenuGroup,
  MenuItem,
  List,
  ListItem
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
 
  //Estadisticas
  const [nodos, setNodos] = useState(0);
  const [profundidad, setProfundidad] = useState(0);
  const [tiempo, setTiempo] = useState(0);
  const [costo, setCosto] = useState("0");
  
 
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
         setSelectedFile(data.arrays);
         setNodos(data.nodes);
         setProfundidad(data.depth);
         setTiempo(data.time);
         setCosto(data.cost)

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

         <HStack spacing={2}>
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
       
        
        </HStack>    

        
      

        <HStack spacing={7}>
          <Box borderRadius='md' bg='purple.300' color='white' px={2} py={1}>Nodos: {nodos} </Box>
          <Box borderRadius='md' bg='purple.300' color='white'px={2} py={1}>Profundidad: {profundidad}</Box>
          <Box borderRadius='md' bg='purple.300' color='white'px={2} py={1}>Tiempo:  {tiempo}</Box>
          <Box borderRadius='md' bg='purple.300' color='white'px={2} py={1}>Costo:  {costo}</Box>
        </HStack>
        
      
        <BoxGrid matriz={map} />

        <Button  
          rightIcon={<Icon as = {FaPlay} />}
          colorScheme='whatsapp'
          onClick={handleClickRun}>
            Start
        </Button>

     

      </VStack>
      </Center>
  )
}

export default App
