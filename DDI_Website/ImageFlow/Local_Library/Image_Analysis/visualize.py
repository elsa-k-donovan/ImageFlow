import os
import json
import shutil
import ntpath


class visualize():
    output_path = "data/clusters/"
    input_path = "data/clustering_output.txt"
    image_extensions = ['.jpg', '.png', '.jpeg', '.gif']

    def __init__(self, input_p):
        self.all_images = [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_p) for f in filenames if os.path.splitext(f)[1].lower() in self.image_extensions]

    def load_clusters_to_folder(self, cluster_json=None):
        if cluster_json == None:
            cluster_json = []
            with open(self.input_path, 'r') as f:
                for line in f:
                    cluster_json.append(json.loads(line))

        clustered_images = []
        num_clustered_images = 0
        for line in cluster_json:
            cluster = line['cluster_no']

            # this is for the outliers! so we can ignore them!
            if cluster == -1:
                continue
            
            images_in_cluster = line['images']
            print("Cluster = %d Images = %d" %(cluster, len(images_in_cluster)))

            num_clustered_images = num_clustered_images + len(images_in_cluster)

            cluster_dir = self.output_path + "cluster" + str(cluster)

            try:
                shutil.rmtree(cluster_dir)
            except:
                pass
            os.makedirs(cluster_dir)
            for image in images_in_cluster:       
                shutil.copy2(image, cluster_dir+"/"+ntpath.basename(image))
                clustered_images.append(image)

        non_clustered_images = []
        for img in self.all_images:
            if not img in clustered_images:
                non_clustered_images.append(img)

        non_cluster_dir = self.output_path + "non_cluster"
        try:
            shutil.rmtree(non_cluster_dir)
        except:
            pass
        os.makedirs(non_cluster_dir)

        for img in non_clustered_images:
            shutil.copy2(image, non_cluster_dir+"/"+ntpath.basename(img))

        print("number of all images = " + str(len(self.all_images)))
        print("number of non clustered images = " + str(len(non_clustered_images)))
        print("number of clustered images = " + str(len(clustered_images)))
        return


