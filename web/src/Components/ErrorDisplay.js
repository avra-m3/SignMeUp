import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import {withStyles} from '@material-ui/core/styles';
import LinearProgress from "../../node_modules/@material-ui/core/LinearProgress/LinearProgress";
import Card from "../../node_modules/@material-ui/core/Card/Card";
import CardActionArea from "../../node_modules/@material-ui/core/CardActionArea/CardActionArea";
import CardContent from "../../node_modules/@material-ui/core/CardContent/CardContent";
import CardActions from "@material-ui/core/CardActions";


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


class ErrorDisplay extends Component {

    state = {};

    static propTypes = {
        onContinue: PropTypes.func.isRequired,
        onResend: PropTypes.func.isRequired,
        error: PropTypes.shape({
            code: PropTypes.number,
            message: PropTypes.string,
            status: PropTypes.string
        }).isRequired
    };

    render() {
        const {classes, error} = this.props;

        return (
            <div className={classes.root}>
                <div className={classes.progress}>
                    <LinearProgress color="secondary" variant="determinate" value={100}/>
                </div>
                <div className={classes.paper}>
                    <Card>
                        <CardActionArea
                        >
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Unfortunately, we were unable to process that request
                                </Typography>
                                <Typography component="p">
                                    {error.code !== undefined &&
                                    <span>The server rejected the image with the following message: "{error.message}"</span>}
                                    {error.code === undefined &&
                                    <span>The server rejected the provided image with no information provided</span>}
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                        <CardActions>
                            <Button size="small" color="primary" onClick={this.props.onContinue}>
                                Continue
                            </Button>
                            <Button size="small" color="secondary" disabled={error.code !== undefined}
                                    onClick={this.props.onResend}>
                                Try again (resend)
                            </Button>
                        </CardActions>
                    </Card>
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(ErrorDisplay);