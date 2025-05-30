export function CardDisplay({ images }) {
  if (!images || images.length === 0) return null;

  return (
    <div className="grid-container">
      {images.map((src, index) => {
        if (!src) return null;

        return <img key={index} src={src} alt={`Shotcard ${index}`} />;
      })}
    </div>
  );
}