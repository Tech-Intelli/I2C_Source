
import ChooseCaption from './components/ChooseCaption/ChooseCaption';
import { Layout } from './components/LandingPage/Layout';
import { UploadFile } from './components/UploadFile/UploadFile';
import { BrowserRouter,Routes,Route } from 'react-router-dom';
import Caption from './components/caption/Caption';
function App() {
  const onFileChange = (files) => {
    console.log(files);
}
  return (
    <div className="App">


<BrowserRouter>
      <Routes>
          <Route path="/" element={<Layout />}></Route>
     </Routes>
     <Routes>
     
          <Route path="/uploadfile" element={<UploadFile onFileChange={(files) => onFileChange(files)}  />} />
     </Routes>
     <Routes>
          <Route path="/generatecaption" element={<ChooseCaption />} />
     </Routes>
     <Routes>
          <Route path="/caption" element={<Caption />} />
     </Routes>
          {/* <Route path="*" element={<NoPage />} /> */}
    </BrowserRouter>
    </div>
  );
}

export default App;
