import { 
  Box,
  Text,
  Icon, 
  Center, 
  Button,  
  VStack, 
  Heading} from '@chakra-ui/react'



import {FaPlay}  from "react-icons/fa6";

import BoxGrid from './components/BoxGrid';
import UploadButton from './components/UploadButton';

import { useEffect, useState } from 'react';


function App() {

  const  matrix =[ [0,0,2],
                   [0,1,0],
                   [3,0,0],];

  const matrix1 = [
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [0, 1, 0, 2, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 5, 4, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [3, 0, 0, 0, 2, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
  ];
  
  const matrix2 = [
    [0, 0, 0, 5, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  ];

  const [map, setMap] = useState(matrix);
  const [clickRun, setClickRun] = useState(false);
  const [miValor, setMiValor] = useState('');
  
  /* 
  useEffect(() => {

   const sessionMap = localStorage.getItem('matrizMap');
    console.log(sessionMap)

    if (sessionMap) {
      setMiValor(sessionMap)
      console.log('abrio el localstorage desde app',sessionMap)
    }

  },[miValor])
  */

  useEffect(()  => {
    if(clickRun) {
      console.log("entre al run")
      const intervalId = setInterval(() => {
        setMap(matrix1);
      }, 2000);

      return () => clearInterval(intervalId);
    }
    
  }, [clickRun]);

  function handleClickRun() {
    setClickRun(true);
    
  }


  return (
      <Center h='100%'>
      <VStack gap={5}>  

        <Heading  color='black'>Algoritmos de Busqueda</Heading>

        <UploadButton/>
      
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
