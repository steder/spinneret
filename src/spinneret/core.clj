(ns spinneret.core
  (:gen-class))
;;  (:require [clojure.java.io :as io]))

(require '[clj-yaml.core :as yaml])
(use '[clojure.string :only (join)])

(defn url-join [coll]
  (join "/" (filter (fn [x] (and x (not (empty? x)))) coll))
  )

(defn print-urls-helper [base sitemap]
  (doseq [[k v] (map identity sitemap)]
    (println (url-join [base (name k)]))
    (print-urls-helper (url-join [base (name k)]) v)
    )
  )

(defn print-urls [sitemap_url]
  "just print out all the urls in the sitemap"
  (let [sitemap (yaml/parse-string (slurp sitemap_url))]
    (print-urls-helper "http://www.threadless.com" sitemap))
  )

(defn get-urls-helper [base sitemap]
  "recursively return urls from the sitemap"
  (map (fn [x] (conj (get-urls-helper (url-join [base (name (key x))]) (val x)) (url-join [base (name (key x))]))) sitemap)
  )

(defn get-urls [sitemap_url]
  "return a list of urls in the sitemap"
  (get-urls-helper "http://www.threadless.com" (yaml/parse-string (slurp sitemap_url)))
  )

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  ;; work around dangerous default behaviour in Clojure
  (alter-var-root #'*read-eval* (constantly false))
  (println "Reading sitemap.yml")
  ;;(println (-> (java.io.File. ".") .getAbsolutePath))
  (print-urls "sitemap.yaml")
  (doseq [[x] (get-urls "sitemap.yaml")] (println x))
  )
