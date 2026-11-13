

export class APIResponseError extends Error {
  constructor(message: string) {
    super(message);
  }
}

export class UnauthenticatedError extends Error {
  constructor(message: string) {
    super(message);
  }
}