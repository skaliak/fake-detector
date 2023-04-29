"""implementation of the gRPC server for the fake detection service"""

import sys
sys.path.append("..")

from concurrent import futures
import logging
import grpc
import fakedetect_pb2
import fakedetect_pb2_grpc

import main.fake_detector as fake_detector
import main.data_layer as data_layer

class FakeDetect(fakedetect_pb2_grpc.FakeDetectorServiceServicer):
    """implementation of the gRPC server for the fake detection service"""
    def __init__(self) -> None:
        logging.info("FakeDetect.__init__()")
        self._detector = fake_detector.FakeDetector(data_layer.HardCodedDataAccess())
    
    def CheckUsername(self, request, context):
        """check single username"""
        logging.info("CheckUsername: {}".format(request.username))
        response = fakedetect_pb2.CheckUsernameResponse()
        response.is_fake = self._detector.is_fake(request.username)
        return response
    
    def CheckUsernames(self, request, context):
        """check multiple usernames"""
        logging.info("CheckUsernames: {}".format(request.usernames))
        # TODO: implement request size limits
        response = fakedetect_pb2.CheckUsernamesResponse()
        response.is_fake.extend([username for username in request.usernames if self._detector.is_fake(username)])
        return response
    
def serve():
    """start the gRPC server"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fakedetect_pb2_grpc.add_FakeDetectorServiceServicer_to_server(FakeDetect(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    logging.info("server stopped")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='grpc.log', format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    msg = "starting rpc server"
    print(msg)
    logging.info(msg)
    serve()
    