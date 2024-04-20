import { useEffect, useState } from "react";
import "./App.css";

const TRY_LIST = ["عذاب النار", "غض البصر", "شكر الله", "فريضة الحجاب"];
function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [trySearchTerm, setTrySearchTerm] = useState("");
  const [searchResult, setSearchResult] = useState([]);
  useEffect(() => {
    if (trySearchTerm) search();
  }, [trySearchTerm]);

  async function search() {
    const req = await fetch(
      `http://localhost:5000/search?query=${searchTerm}`,
      {
        method: "GET",
      }
    );
    const res = await req.json();
    console.log(res.data);
    setSearchResult(res.data);
  }
  return (
    <div className="App">
      <div id="bg"></div>
      <div id="box-wrapper">
        <div id="box">
          <div id="box-cover"></div>
          <div id="box-content">
            <h1>إبحث في القرآن الكريم</h1>
            <p>ادخل جمله للبحث عن الآيات المرتبطه بها في القرآن الكريم</p>
            <div id="search-box">
              <input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyUp={(e) => e.key === "Enter" && search()}
                type="text"
                placeholder="ابحث هنا"
              />
              <button onClick={() => search()}>ابحث</button>
            </div>
            <div id="try">
              <p>جرب مثلاً: </p>
              <ul>
                {TRY_LIST.map((item, index) => (
                  <li
                    key={index}
                    onClick={() => {
                      setSearchTerm(item);
                      setTrySearchTerm(item);
                    }}
                  >
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <table>
              <thead>
                <tr>
                  <th>السورة</th>
                  <th>رقم الآية</th>
                  <th>الموضوع الرئيسي</th>
                  <th>الموضوع الفرعي</th>
                  <th>الآية</th>
                  <th>التفسير</th>
                </tr>
              </thead>
              <tbody>
                {searchResult.map((item, index) => (
                  <tr key={index}>
                    <td>{item.surah}</td>
                    <td>{item.verse_number}</td>
                    <td>{item.main_topic}</td>
                    <td>{item.sub_topic}</td>
                    <td>{item.ayah}</td>
                    <td>{item.tafseer}</td>
                  </tr>
                ))}
                {searchResult.length === 0 && (
                  <tr>
                    <td colSpan="6">لا توجد نتائج بحث</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
