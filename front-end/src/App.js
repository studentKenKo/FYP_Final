import logo from './logo.svg';
import './App.css';
import "antd/dist/antd.css";
import React, { useState, useEffect } from 'react';
import http from './http-common';
import { Layout, Col, Row } from 'antd';
import { Input, Space } from 'antd';
import MovieCards from './components/MovieCards'
import { Tag } from 'antd';

const { Search } = Input;

const { Header, Footer, Sider, Content } = Layout;

function App() {

  useEffect(() => {
    http.get('movies')
    .then(({data}) => {
      // console.log(data.result)
      setMovieList(data.result)
      setPersonList([])
      setDateList([])
      setTokenList([])
    }).catch((error) => {
      setLoading(false)
    }).then(()=> {
      setLoading(false)
    })
  },[]);
  const [ loading, setLoading ] = useState(true);
  const [ movieList, setMovieList ] = useState([]);
  const [ personList, setPersonList ] = useState([]);
  const [ dateList, setDateList ] = useState([]);
  const [ tokenList, setTokenList ] = useState([]);
  const onSearch = (value) => {
    console.log(value)
    http.get('movie/'+ value)
    .then(({data}) => {
      setTokenList(data.token)
      setMovieList(data.result)
      setPersonList(data.person)
      setDateList(data.date)
    }).catch((error) => {
      setLoading(false)
    }).then(()=> {
      setLoading(false)
    })
    console.log(value);
  }
  return (
    <div>
    <Layout>
    <Layout
  >
      <Header
        className="site-layout-background"
        style={{ backgroundColor: "#888888" }}
      >
        <Row>
          <Col span={1}><img width="40" src={"https://icon-library.com/images/movie-icon/movie-icon-26.jpg"}/></Col>
          <Col span={23}><h1>Movie Searching</h1></Col>
        </Row>
      </Header>
      <Content
       style={{
        textAlign: 'center',
      }}>
        <>
        <Row>
          <Col span={18} offset={3}>
            <br/>
            <br/>
            <br/>
                <Search
                  addonBefore=""
                  placeholder="Free text Here"
                  onSearch={onSearch}
                  style={{
                    width: 304,
                  }}
                />
            <br/>
            <br/>
            <br/>
            <br/>

            {!loading && tokenList.length !== 0 && <span>Tokens: {tokenList.map((token, index) => <Tag>{token}</Tag>)}</span>}<br/>
            {!loading && personList.length !== 0 && <span>Keywords(Person): {personList.map((person, index) => <Tag>{person}</Tag>)}</span>}<br/>
            {!loading && dateList.length !== 0 && <span>Keywords(Date): {dateList.map((date, index) => <Tag>{date}</Tag>)}</span>}<br/>
            {!loading && movieList.length == 0 && <span>Sorry Related Movies not found.</span>}<br/>
            {!loading && <MovieCards movies={movieList}/>}
          </Col>
        </Row>
        </>
      </Content>
      <Footer
        style={{
          textAlign: 'center',
        }}
      >
        Movie Searching ©2022 Created by Ko Long
      </Footer>
    </Layout>
  </Layout>
  </div>
  );
}

export default App;