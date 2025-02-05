function Car(props) {
    return <h2>I am aa { props.brand }!</h2>;
  }
  
  function Garage() {
    return (
      <>
        <h1>Who lives in my garage?</h1>
        <Car brand="Ford" />
      </>
    );
  }
  
  const root = ReactDOM.createRoot(document.getElementById('mydiv'));
  root.render(<Garage />);