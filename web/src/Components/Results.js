import React, {Component} from 'react';
import * as PropTypes from "prop-types";
import Paper from '@material-ui/core/Paper';
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


class Results extends Component {

    state = {
    };

    static propTypes = {
        onContinue: PropTypes.func.isRequired,
        registration: PropTypes.shape({
            id: PropTypes.number,
            expiry: PropTypes.string,
            club: PropTypes.shape({
                id: PropTypes.number,
                name: PropTypes.string,
                description: PropTypes.string
            }),
            user: PropTypes.shape({
                email: PropTypes.string,
                first_name: PropTypes.string,
                last_name: PropTypes.string,
                student_id: PropTypes.string
            })
        }).isRequired
    };

    render() {
        const {classes, registration} = this.props;

        return (
            <Paper className={classes.root}>
                <div>{registration.id}</div>
                <div>{registration.user.email}</div>
                <div>{registration.user.student_id}</div>
                <div>{`${registration.user.first_name} ${registration.user.last_name}`}</div>
                <div>{registration.expiry}</div>
            </Paper>
        )
    }
}

export default withStyles(styles)(Results);