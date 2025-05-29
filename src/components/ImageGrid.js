// ImageGrid.js
import React from 'react';
import './ImageGrid.css';

const ImageGrid = ({ images }) => {
  return (
    <div className="grid-container">
      {images.map((imgPath, index) => (
        <img
          key={index}
          src={`http://localhost:5000${imgPath}`} // Adjust for your backend
          alt={`img-${index}`}
        />
      ))}
    </div>
  );
};

export default ImageGrid;