import React from 'react';
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import AccountCircle from '@material-ui/icons/AccountCircle';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import Snackbar from "@material-ui/core/Snackbar";
import StyledSnacks from "./StyledSnacks";

const style ={
    root: {
        flexGrow: 1,
    },
    grow: {
        flexGrow: 1,
    },
    menuButton: {
        marginLeft: -12,
        marginRight: 20,
    },
};

class Navbar extends React.Component {
    static propTypes = {
        onLogOff: PropTypes.func.isRequired,
        isAuthorized: PropTypes.bool.isRequired,
        onHideMessage: PropTypes.func.isRequired,
        message: PropTypes.shape({
            text: PropTypes.string,
            type: PropTypes.string,
            show: PropTypes.bool
        }).isRequired
    };

    state = {
        auth: true,
        anchorEl: null,
    };

    handleMenu = event => {
        this.setState({anchorEl: event.currentTarget});
    };

    handleClose = () => {
        this.setState({anchorEl: null});
    };

    render() {
        const {classes, message, isAuthorized} = this.props;
        const {anchorEl} = this.state;
        const open = Boolean(anchorEl);


        return (
            <div className={classes.root}>
                <AppBar position="static">
                    <Toolbar>
                        <IconButton className={classes.menuButton} color="inherit" aria-label="Menu">
                            <MenuIcon/>
                        </IconButton>
                        <Typography variant="h6" color="inherit" className={classes.grow}>
                            SignMeUp
                        </Typography>
                        {isAuthorized && (
                            <div>
                                <IconButton
                                    aria-owns={open ? 'menu-appbar' : undefined}
                                    aria-haspopup="true"
                                    onClick={this.handleMenu}
                                    color="inherit"
                                >
                                    <AccountCircle/>
                                </IconButton>
                                <Menu
                                    id="menu-appbar"
                                    anchorEl={anchorEl}
                                    anchorOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    transformOrigin={{
                                        vertical: 'top',
                                        horizontal: 'right',
                                    }}
                                    open={open}
                                    onClose={this.handleClose}
                                >
                                    <MenuItem disabled={true}>About</MenuItem>
                                    <MenuItem onClick={this.doLogOff}>Log Out</MenuItem>

                                </Menu>
                            </div>
                        )}
                    </Toolbar>
                </AppBar>
                <Snackbar
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'left',
                    }}
                    open={message.show}
                    autoHideDuration={6000}
                    onClose={this.props.onHideMessage}
                >
                    <StyledSnacks
                        onClose={this.props.onHideMessage}
                        variant={message.type}
                        message={message.text}
                    />
                </Snackbar>
            </div>
        );
    }
    doLogOff = () => {
        this.handleClose();
        this.props.onLogOff();
    }
}

export default withStyles(style)(Navbar);