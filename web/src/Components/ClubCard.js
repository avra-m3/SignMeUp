import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

const styles = {
    card: {
        maxWidth: 345,
    },
    media: {
        maxHeight: 140,
        objectFit: 'cover',

    },
};

class ClubCard extends React.Component {
    static propTypes = {
        name: PropTypes.string.isRequired,
        abbreviation: PropTypes.string.isRequired,
        description: PropTypes.string.isRequired,
        onSelect: PropTypes.func.isRequired,
        image: PropTypes.string,
        classes: PropTypes.object.isRequired,
    };

    render() {
        const {classes, name, description, onSelect, key, abbreviation, image} = this.props;
        return (
            <Card key={key} className={classes.card}>
                <CardActionArea>
                    {image && <CardMedia
                        className={classes.media}
                        title={name}
                        image={image}

                    />}
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            {name}
                        </Typography>
                        <Typography component="p">
                            {description}
                        </Typography>
                    </CardContent>
                </CardActionArea>
                <CardActions>
                    <Button size="small" color="primary" onClick={onSelect}>
                        Continue as {abbreviation.toUpperCase()}
                    </Button>
                </CardActions>
            </Card>
        );
    }
}


export default withStyles(styles)(ClubCard);

