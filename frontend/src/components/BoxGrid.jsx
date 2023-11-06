import { 
    Box,  
    SimpleGrid, 
    useBreakpointValue } from '@chakra-ui/react'

import PropTypes from 'prop-types';

  
  
  function BoxGrid({matriz}) {
  
    const boxSize = useBreakpointValue({ base: '4', sm: '7', md: '7', lg: '8' })
    const spacingSize = useBreakpointValue({ base: '1', sm: '1.5'})
  
    const colors = {
      0: 'gray.300',
      1: 'blue.400',
      2: 'orange',
      3: 'purple.400',
      4: 'purple.400',
      5: 'green.400',
      6: 'red.500',
    };
  
    return (
    
    <SimpleGrid 
      columns={matriz[0].length} 
      spacing={spacingSize} 
      alignItems='center'>
        
        {matriz.map( (row, rowIndex) => (
              row.map((item, colIndex) => (
                <Box 
                  key={`${rowIndex}-${colIndex}`} 
                  borderRadius='md' 
                  bg={colors[item]} 
                  h={boxSize} 
                  w={boxSize}/> 
            ))))}

    </SimpleGrid>  
    
  
    )
  }

  BoxGrid.propTypes = {
    matriz: PropTypes.arrayOf(PropTypes.arrayOf(PropTypes.number)).isRequired,
  };
  
  export default BoxGrid;
  