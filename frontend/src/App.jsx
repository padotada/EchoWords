import { useState } from 'react'
import './App.css'

function App() {
  const [defClick, setDefClick] = useState(false);
  const [msg, setMsg] = useState("");
  const [translation, setTranslation] = useState("");
  const [analysis, setAnalysis] = useState([]);
  const [words, setWords] = useState([]);
  const [hover_array, setHoverArray] = useState([]);

  const handleClear = () => {
    setMsg("");
    setWords([]);
    setAnalysis([]);
    setTranslation("");
    setHoverArray([]);
  };
  async function getData(){
    console.log("get data started");
    // url = "http://127.0.0.1:5000/tran"
    const temp = await fetch("http://127.0.0.1:5000/api/translate", {
      method: "POST",
      headers: {
        "Content-type" : "text/plain",
      },
      body: msg,
    });
    const res = await temp.text();
    setTranslation(res);
    console.log("F");
    console.log(res);
    console.log(msg);

    console.log("ran res", res);
    console.log(msg)
    const w_list = await fetch("http://127.0.0.1:5000/api/translate/words", {
      method: "POST",
      headers:  {
        "Content-type" : "application/json",
      },
      body: msg,
    });
    const res3 = await w_list.json();
    //console.log('hi');
    //console.log(res3);
    setWords(res3);
    setHoverArray(Array(res3.length).fill(false))

    //console.log(words);
    
  }
  async function unpack() {
    const sentence = await fetch("http://127.0.0.1:5000/api/analyze/sentence",{
      method: "POST",
      headers:  {
        "Content-type" : "application/json",
      },
      body: msg,
    });
    let res2 = await sentence.json();
    console.log("Analysis response:", res2);
    console.log("Response type:", typeof res2);
    console.log("Is array:", Array.isArray(res2));
    if(!Array.isArray(res2)) res2 = [res2]
    setAnalysis(res2);
  }
  return (
    <>
      <h1 className = "Title">EchoWords</h1>
      
      <div className="outer-div">
         {!words ? <div><textarea className="box placeholder1" placeholder="Enter Text" onChange={(e) => setMsg(e.target.value)} value={msg}></textarea></div>
          : <div className="box2">{
            words.map((e, i) => {
              const elem = Object.entries(e)[0];
              return (<div className='definition'>
              {hover_array[i] && <div className="hover-word">{elem[1]}</div>}
              <div style={hover_array[i] ? {"backgroundColor": "yellow"} : {}} className = "word" onMouseEnter={() => setHoverArray((arr) => [...arr.slice(0, i), true, ...arr.slice(i+1)])} onMouseLeave={() => setHoverArray((arr) => [...arr.slice(0, i), false, ...arr.slice(i+1)])}> {elem[0]} </div>
              </div>)
            }
          )}</div>}
        
        {/* <textarea className="box" readOnly> </textarea>*/}
        <div className="box">{translation}</div>
      </div>
      <div className="btn-container1">
      <button className="first-btn" disabled={!msg.trim()} onClick={()=>getData()} >Translate</button>
      <button className="first-btn" onClick={handleClear}>Clear</button>
      </div>
      <div className="lower-modules">
        <div className="btn-container2">
          <button className="second-btn" onClick={()=>unpack()}>Analyze</button>
          {/* <button className="second-btn" onClick={()=>setDefClick(false)}>Definitions</button>  */}
        </div>
        
        {!defClick ? <div className="lower-box">
          {analysis &&
          analysis.map((a, i) => {
            const original = Object.entries(a);
            const reordered = [original[2], original[3], original[1], original[0]]
            return <div key={i} className="analysis-line">{reordered.map((b) => {
              return(
                <div key={b[1]}><b>{b[0]}</b>{`: ${b[1]}`}</div>
              )
            })}</div>
          })
      }
      </div> : <div className="lower-box">Definition</div>}
        
      </div>
    </>
  )
}

export default App;
