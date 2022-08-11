import React from 'react';
import { Divider, Row, Col, Button } from 'antd';
import 'antd/dist/antd.css';
import { Card, Avatar } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';
import { VideoCameraAddOutlined } from '@ant-design/icons';

export default ({movie}) => {
  console.log('efw', movie)
  let type
  if (movie[5] !== "Null" && movie[5] !== undefined) {
    type = movie[5].split(/[, ]+/);
  }
//   if (movie.actors !== undefined) {
//     movie.actors = movie.actors.split(/[, ]+/);
//     console.log('movie.actors  ', movie.actors)
//   }
  // console.log(movie.type)
//   let birth = movie.birthday? new Date(movie.birthday).toISOString().split('T')[0] : ""
  return (
    <Card
      // onClick={() => {
      //   console.log("go")
      // }}
      style={{width: 250, margin: "auto"}}
      hoverable={true}
      cover={
        movie[6] !== ''?
          <img width="250" style={{ objectFit: "cover"}} src={movie[6]}/>
          : <div style={{ width: 250, height: 250, display: "flex", justifyContent: "center", alignItems: "center", backgroundColor: "#f3f2f2" }}><LoadingOutlined /></div>
      }
    >
      <Card.Meta
        // avatar={<Avatar src="https://joeschmoe.io/api/v1/random" />}
        title={movie[1]}
        description={
        <>
            {movie[8] && <p> {movie[8].substring(0, 100) + '...'}</p>}
            <p>runtime: {movie[4]}</p>
            <p>Release Date: {movie[2]}</p>
            <p>Story: {movie[10].substring(0, 300) + '...'}</p>
            {movie[7] !== "" && movie[7] !== "Null" 
              && <Button type="primary" icon={<VideoCameraAddOutlined />} size={'large'} onClick={() => window.open(movie[7], "_blank")}>
              Watch Trailer
              </Button>
        }
        <br/>
        <br/>
            {type && type.map((t, index) => (
                <Button type="primary" shape="round" size={'small'}>
                {t}
            </Button>
            ))
            }
            
        </>
        }
      />
    </Card>
  )
  };