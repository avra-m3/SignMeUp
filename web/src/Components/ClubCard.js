import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import CardHeader from "../../node_modules/@material-ui/core/CardHeader/CardHeader";
import Avatar from "../../node_modules/@material-ui/core/Avatar/Avatar";
import red from "@material-ui/core/es/colors/red";

const styles = {
    card: {
        maxWidth: 300,
        margin: "20px 5px"
    },
    media: {
        maxHeight: 140,
        objectFit: 'cover',

    },
    avatar: {
        backgroundColor: red[500],
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
        const {classes, name, description, onSelect, key, abbreviation} = this.props;
        return (
            <Card key={key} className={classes.card}>
                <CardActionArea>
                    <CardHeader
                        avatar={
                            <Avatar aria-label="Logo" className={classes.avatar}>
                                {abbreviation.toUpperCase()}
                            </Avatar>
                        }
                        title={name}
                        subheader="RUSU Affiliated"
                    />
                    <CardContent>
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

