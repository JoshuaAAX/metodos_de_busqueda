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
  ListItem,
  Card,
  CardBody,
  Spacer
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
 
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [map, setMap] = useState(matrix);
  const [clickRun, setClickRun] = useState(false);
 
  //Estadisticas
  const [nodos, setNodos] = useState(0);
  const [profundidad, setProfundidad] = useState(0);
  const [tiempo, setTiempo] = useState(0);
  const [costo, setCosto] = useState("0");

  //valor del algoritmo
  const [selectedAlgorithm, setSelectedAlgorithm] = useState(0);
  
 
  function handleClickRun() {
    setClickRun(true);
  }

  // Actualiza el estado con el valor seleccionado del Select
  function handleSelect(event) {
    setSelectedAlgorithm(parseInt(event.target.value)); 
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
        const lines = content.replace(/\r/g,'').trim().split(/\n/)
        const trimmedLines = lines.map(line => line.trim());
        const matriz = trimmedLines.map(row => row.split(" ").map(number => parseInt(number)));
        

        setMap(matriz)
        console.log(matriz);
    };

    reader.readAsText(file);


    
    if(file) {
      
      const formData = new FormData
      formData.append("file", file)

      fetch(`http://localhost:8000/uploadfile/${selectedAlgorithm}`, {
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
        
        <Card bg='purple.200' w='100%' >
         <CardBody textAlign='center'>
           <Heading  color='white'>Algoritmos de Busqueda</Heading>
         </CardBody>
        </Card> 


        <Card bg='blue.200' w='100%' >
          <CardBody>
            <HStack spacing={2}>
                
                <Select 
                  variant='filled' 
                  placeholder='Seleccione un algoritmo primero' 
                  value={selectedAlgorithm} 
                  onChange={handleSelect}>
                  <option value='' disabled>Busqueda no informada</option>
                  <option value={1}>Preferente por Amplitud</option>
                  <option value={2}>Costo uniforme</option>
                  <option value={3}>Preferente por Profundidad</option>
                  <option value='' disabled>Busqueda informada</option>
                  <option value={4}>Avara</option>
                  <option value={5}>A*</option>
                </Select>

                <Input 
                  display='none'
                  type='file'
                  accept='.txt'
                  ref={fileInputRef}
                  onChange={handleFileSelected} />
          
                <Button 
                  px = {6}
                  type='file' 
                  rightIcon={<Icon as={FiUpload}/>} 
                  colorScheme='blue'
                  onClick={handleFileButton}
                  isDisabled={!selectedAlgorithm}>
                    Upload
                </Button>

            </HStack>  
          </CardBody>
        </Card>  

        <Center><BoxGrid matriz={map} /></Center>
        

        <Card bg='blue.100' w='100%'  >
          <CardBody>
            <HStack spacing={7} mb={4}>
              <Box borderRadius='md' bg='purple.300' color='white' px={2} py={1}>Nodos: {nodos} </Box>
              <Box borderRadius='md' bg='purple.300' color='white'px={2} py={1}>Profundidad: {profundidad}</Box>
              <Box borderRadius='md' bg='purple.300' color='white'px={2} py={1}>Tiempo:  {tiempo}</Box>
              <Box borderRadius='md' bg='purple.300' color='white'px={2} py={1}>Costo:  {costo}</Box>
            </HStack>
            
           
          
            <Button  
              w='100%'
              rightIcon={<Icon as = {FaPlay} />}
              colorScheme='whatsapp'
              onClick={handleClickRun}
              isDisabled={!selectedFile}>
                Start
            </Button>
          </CardBody>
        </Card>

      </VStack>
      </Center>
  )
}

export default App
