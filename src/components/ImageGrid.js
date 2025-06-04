
import React from 'react';
import './ImageGrid.css';

const ImageGrid = ({ images }) => {
  return (
    <div className="grid-container">
      {images.map((imgPath, index) => (
        <img
          key={index}
          src={`${process.env.REACT_APP_API_URL}${imgPath}`} 
          alt={`img-${index}`}
        />
      ))}
    </div>
  );
};

export default ImageGrid;