import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import {withStyles} from '@material-ui/core/styles';


const styles = theme => ({
    root: theme.mixins.gutters({
        paddingTop: 16,
        paddingBottom: 16,
        marginTop: theme.spacing.unit * 3,
    }),
    container: {
        display: 'flex',
        flexWrap: 'wrap',
        flexDirection: "column",
        margin: "auto",
        maxWidth: "200px"
    },
    textField: {
        marginLeft: theme.spacing.unit,
        marginRight: theme.spacing.unit,
        width: 200,
    },
    menu: {
        width: 200,
    },
});


class ErrorDisplay extends Component {

    state = {};

    static propTypes = {
        onContinue: PropTypes.func.isRequired,
        error: PropTypes.shape({
            code: PropTypes.number,
            message: PropTypes.string,
            status: PropTypes.string
        }).isRequired
    };

    render() {
        const {classes, error} = this.props;

        return (
            <Paper className={classes.root}>
                <Typography>A {error.code} Error occurred while processing this request</Typography>
                <div>
                    <Typography>{error.status}</Typography>
                    <Typography>{error.message}</Typography>
                </div>
                <Button onClick={this.props.onContinue}/>
            </Paper>
        )
    }
}

export default withStyles(styles)(ErrorDisplay);