import { Row, Col} from 'antd';
import MovieCard from './MovieCard';
function MovieCards({movies}) { 
    console.log('cards ', movies)
    return (
        <>
        <Row justify="center" gutter={[0, 24]}>
            {movies.map((movie, index) => (
                <Col key={index} className="gutter-row" span={6}>
                    <MovieCard movie={movie} />
                </Col>
            ))
            }
        </Row>
        </>
    );
}
export default MovieCards;