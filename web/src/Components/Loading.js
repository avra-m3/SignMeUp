import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import {withStyles} from '@material-ui/core/styles';
import LinearProgress from "../../node_modules/@material-ui/core/LinearProgress/LinearProgress";
import Card from "../../node_modules/@material-ui/core/Card/Card";
import CardActionArea from "../../node_modules/@material-ui/core/CardActionArea/CardActionArea";
import CardContent from "../../node_modules/@material-ui/core/CardContent/CardContent";
import Typography from "@material-ui/core/Typography";


const styles = theme => ({
    root: {
        display: 'flex',
        flexDirection: 'column',
    },
    progress: {
        flexGrow: 1,
    },
    paper: {
        ...theme.mixins.gutters(),
        paddingTop: theme.spacing.unit * 2,
        paddingBottom: theme.spacing.unit * 2,
    },
});


class CardCapture extends Component {

    state = {};

    static propTypes = {
        onCapture: PropTypes.func.isRequired,
    };

    render() {
        const {classes} = this.props;

        return (
            <div className={classes.root}>
                <div className={classes.progress}>
                    <LinearProgress/>
                </div>
                <div className={classes.paper}>
                    <Card>
                        <CardActionArea
                        >
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Loading
                                </Typography>
                                <Typography component="p">
                                    This might take a bit...
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </div>
            </div>
        )
    }
}

export default withStyles(styles)(CardCapture);