import * as React from 'react'
import { Box, ChakraProvider } from '@chakra-ui/react'
import * as ReactDOM from 'react-dom/client'
import App from './App'

const rootElement = document.getElementById('root')
ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ChakraProvider>
    <Box bg="white" h="100vh" alignContent='center'>
      <App />
    </Box>
    </ChakraProvider>
  </React.StrictMode>
)