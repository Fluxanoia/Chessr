#pragma once

#include <exception>

class InvalidBoardException : public std::exception
{
private:

    const char* message;

public:

    InvalidBoardException(const char* message) : message(message) {}

    virtual const char* what() const throw()
    {
        return this->message;
    }
};

class UnexpectedCaseException : public std::exception
{
private:

    const char* message;

public:

    UnexpectedCaseException(const char* message) : message(message) {}

    virtual const char* what() const throw()
    {
        return this->message;
    }
};
