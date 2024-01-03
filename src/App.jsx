import Feed from "./Feed";
import Nav from "./Nav";

const Page = () => {
  return (
    <>
      <section className="w-full flex-center flex-col">
        <h1 className="head_text text-center">
          Discover & Share
          <br className="max:md-hidden" />
          <span className="orange_gradient text-center">
            Real News with Truth_Finder
          </span>
        </h1>
        <p className="desc text-center">
          Truth_Finder is a Fake News Detection tool for modern world to protect
          themselves from the spread of misinformation.
        </p>
      </section>
      <Feed />
    </>
  );
};

const App = () => {
  return (
    <div>
      {/* <div className="main ">
        <div className="gradient" />
        <main className="app">
          <Nav />
          <Page />
        </main>
      </div> */}
      <div className="main">
        <div className="gradient" />
      </div>
      <main className="app">
        <Nav />
        <Page />
      </main>
    </div>
  );
};

export default App;
